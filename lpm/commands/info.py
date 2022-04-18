from rich.console import Console
from rich.table import Table
from lpm import dnf
from lpm.utils import HumanBytes

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base

def command_info(package_name):
    query = base.sack.query()
    pkg = query.filter(name=package_name)
    pkg = pkg.run()

    if not pkg:
        error_console.print(f"Package [italic]{package_name}[/italic] not found")
        exit()

    pkg = pkg[0]

    table = Table(title="Package Information", expand=True)

    table.add_column(justify="right", style="green")
    table.add_column(style="magenta")

    table.add_row("Name", pkg.name)
    table.add_row("Version", pkg.version)
    table.add_row("Release", pkg.release)
    table.add_row("Architecture", pkg.arch)
    table.add_row("Size", HumanBytes.format(pkg.installsize))
    table.add_row("Source", pkg.sourcerpm)
    if pkg.from_repo != "":
        table.add_row("Repository", pkg.from_repo)
    else:
        table.add_row("Repository", pkg.reponame)
    table.add_row("Summary", pkg.summary)
    table.add_row("URL", pkg.url)
    table.add_row("License", pkg.license)
    table.add_row("Installed", str(pkg.installed))
    if not pkg.group == "Unspecified":
        table.add_row("Group", pkg.group)
    table.add_row("", "")
    table.add_row("Description", pkg.description)
    
    console.print(table)

    
    