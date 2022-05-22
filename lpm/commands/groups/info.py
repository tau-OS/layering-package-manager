from rich.console import Console
from rich.table import Table
from lpm import dnf

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base

def command_group_info(group_name):
    query = base.comps.group_by_pattern(group_name, False)

    if not query:
        error_console.print(f"Group [italic]{group_name}[/italic] not found")
        exit()

    table = Table(title="Group Information", expand=True)

    table.add_column(justify="right", style="green")
    table.add_column(style="magenta")

    table.add_row("Name", query.ui_name)
    table.add_row("Description", query.ui_description)
    table.add_row("", "")

    mandatory_packages = []
    default_packages= []
    for package in query.packages_iter():
        if package.option_type == dnf.comps.MANDATORY:
            mandatory_packages.append(package)
        if package.option_type == dnf.comps.DEFAULT:
            default_packages.append(package)
    if len(mandatory_packages) != 0:
        table.add_row("Mandatory Packages", mandatory_packages[0].name)
        mandatory_packages.pop(0)
        for package in mandatory_packages:
            table.add_row("", package.name)
    table.add_row("", "")
    if len(default_packages) != 0:
        table.add_row("Default Packages", default_packages[0].name)
        default_packages.pop(0)
        for package in default_packages:
            table.add_row("", package.name)
    
    console.print(table)

    
    