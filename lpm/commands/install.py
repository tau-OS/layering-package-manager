from rich.console import Console
from lpm import dnf
from lpm.handlers.format_transaction import format_transaction_summary
from lpm.handlers.install_or_remove_packages import install_or_remove_packages

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base


async def command_install(package_names: tuple[str]):
    query = base.sack.query()
    results = query.installed()

    results = results.filter(name=package_names)

    if len(results) == 1:
        error_console.print(
            f"Package [italic]{results[0].name}[/italic] is already installed"
        )
        exit()
    elif len(results) > 1:
        installed = ", ".join(list(map(lambda x: x.name, results)))
        error_console.print(
            f"Packages [italic]{installed}[/italic] are already installed"
        )
        exit()

    for pkg in package_names:
        base.install(pkg, strict=True)

    try:
        base.resolve()
    except dnf.exceptions.DepsolveError as error:
        error_console.print("An error occured while handling the transaction:")
        print(error)
        exit()

    format_transaction_summary()
    await install_or_remove_packages(list(package_names), [])
