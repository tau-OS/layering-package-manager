from rich.console import Console
from lpm import dnf
from lpm.handlers.format_transaction import format_transaction_summary
from lpm.utils import HumanBytes

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf.base

def command_install(package_name):
    query = base.sack.query()
    results = query.installed()
    results = results.filter(name=package_name)

    if results:
        error_console.print(f"Package [italic]{package_name}[/italic] is already installed")
        exit()

    base.install(package_name)

    base.resolve()

    format_transaction_summary()

    
    

    
    