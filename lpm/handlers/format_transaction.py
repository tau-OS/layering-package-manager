import click
from rich.console import Console
from rich.table import Table
from lpm import dnf
from lpm.utils import HumanBytes

console = Console()
error_console = Console(stderr=True, style="bold red")

base = dnf.base

def format_transaction_summary():
    if not base.transaction.install_set or base.transaction.remove_set:
        error_console.print(f"No packages in transaction")
        exit()

    table = Table(title="Transaction Summary", expand=True)
    colour = "green"
    total_download_size = 0
    total_installed_size = 0

    if base.transaction.remove_set:
        colour = "red"

    table.add_column("Package", justify="right", style=colour)
    table.add_column("Version", style="cyan")
    table.add_column("Architecture", style="yellow")
    table.add_column("Repo", style="magenta")
    table.add_column("Size", justify="left", style="blue")

    if base.transaction.install_set:
        table.add_row("[white]Packages to install:[/white]", "", "", "", "")
        table.add_row("", "", "", "", "")
        for pkg in base.transaction.install_set:
            table.add_row(pkg.name, pkg.version, pkg.arch, pkg.reponame, HumanBytes.format(pkg.downloadsize))
            total_download_size += pkg.downloadsize
            total_installed_size += pkg.installsize
        table.add_row("", "", "", "", "")
        table.add_row("[white]Total packages to install:[/white]", str(len(base.transaction.install_set)), "", "", "")
    if base.transaction.remove_set:
        table.add_row("[white]Packages to remove:[/white]", "", "", "", "")
        table.add_row("", "", "", "", "")
        for pkg in base.transaction.remove_set:
            table.add_row(pkg.name, pkg.version, pkg.arch, pkg.reponame, HumanBytes.format(pkg.installsize))
            total_installed_size += pkg.installedsize
        table.add_row("", "", "", "", "")
        table.add_row("[white]Total packages to remove:[/white]", str(len(base.transaction.remove_set)), "", "", "")

    console.print(table)

    console.print(f"Total Download Size: {HumanBytes.format(total_download_size)}")
    console.print(f"Total Installed Size: {HumanBytes.format(total_installed_size)}")

    click.confirm('Do you understand?', abort=True)