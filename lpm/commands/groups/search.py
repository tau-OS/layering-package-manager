from rich.console import Console
from rich.table import Table
from lpm import dnf

console = Console()

base = dnf.base

def generate_table(title, results):
    table = Table(title=title, expand=True)

    table.add_column("Name", justify="right", style="green")
    table.add_column("Description", style="magenta")

    for group in results:
        table.add_row(group.ui_name, group.ui_description)

    console.print(table)

def command_group_search(group_name):
    query_matched = base.comps.groups_by_pattern(group_name, False)

    generate_table(f"Name Matched: {group_name}", query_matched)

    query = base.comps.groups

    filtered_packages = []
    for group in query:
        if not group in filtered_packages:
            if group_name in group.name:
                filtered_packages.append(group)
            elif group.ui_name is not None and group_name in group.ui_name:
                filtered_packages.append(group)
            elif group.ui_description is not None and group_name in group.ui_description:
                filtered_packages.append(group)

    generate_table(f"Name Contained: {group_name}", filtered_packages)

    
    