from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from lpm import dnf
from lpm.utils import HumanBytes

console = Console()
error_console = Console(stderr=True, style="bold red")

base = dnf.base

def format_transaction_summary():
    if not base.transaction.install_set and not base.transaction.remove_set:
        error_console.print(f"No packages in transaction")
        exit()

    table = Table(title="Transaction Summary", expand=True)
    colour = "green"
    total_download_size = 0
    total_installed_size = 0
    transaction_type = ""

    if base.transaction.remove_set:
        colour = "red"

    table.add_column("Package", justify="right", style=colour)
    table.add_column("Version", style="cyan")
    table.add_column("Architecture", style="yellow")
    table.add_column("Repo", style="magenta")
    table.add_column("Size", justify="left", style="blue")

    if base.transaction.install_set:
        transaction_type = "installed"
        table.add_row("[white]Packages to install:[/white]", "", "", "", "")
        table.add_row("", "", "", "", "")
        for pkg in base.transaction.install_set:
            table.add_row(pkg.name, pkg.version, pkg.arch, pkg.reponame, HumanBytes.format(pkg.downloadsize))
            total_download_size += pkg.downloadsize
            total_installed_size += pkg.installsize
    if base.transaction.remove_set:
        transaction_type = "removed"
        table.add_row("[white]Packages to remove:[/white]", "", "", "", "")
        table.add_row("", "", "", "", "")
        for pkg in base.transaction.remove_set:
            table.add_row(pkg.name, pkg.version, pkg.arch, pkg.reponame, HumanBytes.format(pkg.installsize))
            total_installed_size += pkg.installsize

    console.print(table)

    if base.transaction.install_set:
        console.print(f"Total packages to install: {str(len(base.transaction.install_set))}")

    if base.transaction.remove_set:
        console.print(f"Total packages to remove: {str(len(base.transaction.remove_set))}")

    if total_download_size != 0:
        console.print(f"Total download size: {HumanBytes.format(total_download_size)}")
    console.print(f"Total {transaction_type} size: {HumanBytes.format(total_installed_size)}")

    if not Confirm.ask("Is this ok?"):
        error_console.print("Transaction cancelled")
        exit()