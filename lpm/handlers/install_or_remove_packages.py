import threading
from gi.repository import GLib
import asyncio
from dbus.mainloop.glib import DBusGMainLoop
from typing import Tuple
import dbus
from dbus.connection import Connection
from dbus_next import Variant
from rich.console import Console
from lpm import dnf
from lpm.rpm_ostree import new_rpm_ostree_interface
from rich.progress import Progress, SpinnerColumn

console = Console()
error_console = Console(stderr=True, style="bold red")

base = dnf.base


def run_glib_loop(loop: GLib.MainLoop):
    loop.run()


def new_transaction_peer_interface(address: str):
    DBusGMainLoop(set_as_default=True)

    conn = Connection(address)

    proxy = conn.get_object(
        "org.projectatomic.rpmostree1",
        "/",
    )

    return (
        dbus.Interface(proxy, "org.projectatomic.rpmostree1.Transaction"),
        dbus.Interface(proxy, "org.freedesktop.DBus.Properties"),
        conn,
    )


async def install_or_remove_packages(install: list[str], remove: list[str]):
    if len(install) == 0 and remove == 0:
        error_console.print(f"No packages in transaction")
        exit()

    (interface, _) = await new_rpm_ostree_interface()

    peer_socket = await interface.call_pkg_change(
        {
            "initiating-command-line": Variant("s", "lpm"),
        },
        install,
        remove,
    )

    (peer_interface, peer_properties, peer_conn) = new_transaction_peer_interface(
        peer_socket
    )

    loop = GLib.MainLoop()
    finished_event = asyncio.Event()

    threading.Thread(target=run_glib_loop, args=(loop,)).start()
    asyncio_loop = asyncio.get_running_loop()

    with Progress(SpinnerColumn(), *Progress.get_default_columns()) as progress:
        logs = []
        current_task: int | None = None
        current_progress_task: int | None = None

        def finished_cb(success: bool, error_message: str):
            if not success:
                print(error_message)
            asyncio_loop.call_soon_threadsafe(finished_event.set)
            loop.quit()

        def message_cb(text: str):
            logs.append(text)

        def task_begin_cb(text: str):
            nonlocal current_task
            current_task = progress.add_task(text, start=False)

        def task_end_cb(text: str):
            nonlocal current_task
            if current_task is not None:
                progress.start_task(current_task)
                progress.update(current_task, completed=100)

        def percent_progress_cb(text: str, percentage: int):
            nonlocal current_progress_task
            if current_progress_task == None:
                current_progress_task = progress.add_task(text)

            progress.update(current_progress_task, completed=percentage)

        def progress_end_cb():
            nonlocal current_progress_task
            if current_progress_task != None:
                progress.update(current_progress_task, completed=100)
                current_progress_task = None

        def download_progress_cb(
            time: Tuple[int, int],
            outstanding: Tuple[int, int],
            metadata: Tuple[int, int, int],
            delta: Tuple[int, int, int, int],
            content: Tuple[int, int],
            transfer: Tuple[int, int],
        ):
            pass

        def signature_progress_cb(signature: list[any], commit: str):
            pass

        peer_conn.add_signal_receiver(
            signal_name="Finished",
            handler_function=finished_cb,
        )

        peer_conn.add_signal_receiver(
            signal_name="Message", handler_function=message_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="TaskBegin", handler_function=task_begin_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="TaskEnd", handler_function=task_end_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="PercentProgress", handler_function=percent_progress_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="DownloadProgress", handler_function=download_progress_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="SignatureProgress", handler_function=signature_progress_cb
        )
        peer_conn.add_signal_receiver(
            signal_name="ProgressEnd", handler_function=progress_end_cb
        )

        # TODO: Handle this
        peer_interface.Start()

        await finished_event.wait()
