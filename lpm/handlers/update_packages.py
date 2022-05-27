from dbus_next import Variant
from rich.console import Console
from lpm import dnf
from lpm.rpm_ostree import new_rpm_ostree_interface

console = Console()
error_console = Console(stderr=True, style="bold red")

base = dnf.base


async def update_packages():
    if not base.transaction.install_set and not base.transaction.remove_set:
        error_console.print(f"No packages in transaction")
        exit()

    (interface, _) = await new_rpm_ostree_interface()

    await interface.call_update_deployment(
        {
            "install-packages": Variant(
                "as", list(map(lambda x: x.name, base.transaction.install_set))
            ),
            "remove-packages": Variant(
                "as",
                list(
                    map(lambda x: x.name, base.transaction.remove_set),
                ),
            ),
        },
        {
            "initiating-command-line": Variant("s", "lpm"),
        },
    )

    await interface.call_finalize_deployment({})
