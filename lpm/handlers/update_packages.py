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


async def update_packages():
    if not base.transaction.install_set and not base.transaction.remove_set:
        error_console.print(f"No packages in transaction")
        exit()

    (interface, _) = await new_rpm_ostree_interface()

    peer_socket = await interface.call_pkg_change(
        {
            "initiating-command-line": Variant("s", "lpm"),
        },
        list(map(lambda x: x.name, base.transaction.install_set)),
        list(map(lambda x: x.name, base.transaction.remove_set)),
    )

    (peer_interface, peer_properties, peer_conn) = new_transaction_peer_interface(
        peer_socket
    )

    loop = GLib.MainLoop()
    finished_event = asyncio.Event()

    threading.Thread(target=run_glib_loop, args=(loop,)).start()

    def finished_cb(success: bool, error_message: str):
        print(error_message)
        loop.quit()
        finished_event.set()

    def message_cb(text: str):
        print(text)

    def task_begin_cb(text: str):
        print("oworking...")

    def task_end_cb(text: str):
        print("nyoking...")

    def percent_progress_cb(text: str, percentage: int):
        print("pero...")

    def download_progress_cb(
        time: Tuple[int, int],
        outstanding: Tuple[int, int],
        metadata: Tuple[int, int, int],
        delta: Tuple[int, int, int, int],
        content: Tuple[int, int],
        transfer: Tuple[int, int],
    ):
        print("gura...")

    def signature_progress_db(signature: list[any], commit: str):
        print("fsdfds...")

    def progress_end_db():
        print("I love jade...")

    peer_conn.add_signal_receiver(
        signal_name="Finished",
        handler_function=finished_cb,
    )

    peer_conn.add_signal_receiver(signal_name="Message", handler_function=message_cb)
    peer_conn.add_signal_receiver(
        signal_name="TaskBegin", handler_function=task_begin_cb
    )
    peer_conn.add_signal_receiver(signal_name="TaskEnd", handler_function=task_end_cb)
    peer_conn.add_signal_receiver(
        signal_name="PercentProgress", handler_function=percent_progress_cb
    )
    peer_conn.add_signal_receiver(
        signal_name="DownloadProgress", handler_function=download_progress_cb
    )
    peer_conn.add_signal_receiver(
        signal_name="SignatureProgress", handler_function=signature_progress_db
    )
    peer_conn.add_signal_receiver(
        signal_name="ProgressEnd", handler_function=progress_end_db
    )

    # TODO: Handle this
    peer_interface.Start()

    await finished_event.wait()
