from rich.console import Console
from rich.table import Table
from lpm import dnf

console = Console()

base = dnf.base

def generate_table(title, results):
    table = Table(title=title, expand=True)

    table.add_column("Name", justify="right", style="green")
    table.add_column("Version", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Repository", justify="left", style="red")

    for pkg in results:
        table.add_row(pkg.name, pkg.version, pkg.summary, pkg.reponame)

    console.print(table)

def command_search(package_name):
    query = base.sack.query()
    results = query.filter(name=package_name)

    generate_table(f"Name Matched: {package_name}", results)

    contained_results = query.filter(name__substr=package_name)

    generate_table(f"Name Contained: {package_name}", contained_results)

    
    