import click
from rich.console import Console

console = Console()

@click.group()
@click.option('--override', help="Perform transaction on the base layer", is_flag=True)
@click.version_option("0.1.0")
def cli(override):
    if override:
        # TODO this should be able to be disabled with something like --override=true
        console.print("[bold red]WARNING![/bold red] The [italic]--override[/italic] flag makes changes to your base system." , style="bold")
        console.print("Only use this option if you know what you're doing!")
        click.confirm('Do you understand?', abort=True)

        click.echo("Using base layer")
    """Layered Package Manager"""

@cli.command()
def install():
    """Overlay additional packages"""
    click.echo("Test!")

@cli.command()
def remove():
    """Remove overlayed packages"""
    click.echo("Test!")

@cli.command()
def search():
    """Search package details for the given string"""
    click.echo("Test!")

@cli.command()
def info():
    """Display details about a package or group of packages"""
    click.echo("Test!")

@cli.command()
def rollback():
    """Revert to the previously booted tree.\n
    With the override flag, this resets the base layer"""
    click.echo("Test")