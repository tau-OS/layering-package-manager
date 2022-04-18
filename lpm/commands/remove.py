from rich.console import Console
from lpm import dnf as dnf_utils
from lpm.handlers.format_transaction import format_transaction_summary
import dnf

console = Console()
error_console = Console(stderr=True, style="bold red")
base = dnf_utils.base

def command_remove(package_name):
    query = base.sack.query()
    results = query.installed()
    results = results.filter(name=package_name)

    if not results:
        error_console.print(f"Package [italic]{package_name}[/italic] is not installed")
        exit()

    base.remove(package_name)

    try:
         base.resolve()
    except dnf.exceptions.DepsolveError as error:
        error_console.print("An error occured while handling the transaction:")
        print(error)
        exit()

    format_transaction_summary()

    
    

    
    