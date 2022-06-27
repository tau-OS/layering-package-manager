import dbus
from dbus.connection import Connection
from dbus_next import Variant
from rich.console import Console
from lpm import dnf
from lpm.rpm_ostree import new_rpm_ostree_interface

console = Console()
error_console = Console(stderr=True, style="bold red")

base = dnf.base


def new_transaction_peer_interface(address: str):
    conn = Connection(address)

    proxy = conn.get_object(
        "org.projectatomic.rpmostree1",
        "/",
    )

    return (
        dbus.Interface(proxy, "org.projectatomic.rpmostree1.Transaction"),
        dbus.Interface(proxy, "org.freedesktop.DBus.Properties"),
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

    (peer_interface, peer_properties) = new_transaction_peer_interface(peer_socket)

    print(peer_properties.Get("org.projectatomic.rpmostree1.Transaction", "Title"))
