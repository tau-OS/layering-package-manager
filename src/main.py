import click

@click.group()
@click.option('--override', help="Perform transaction on the base layer", is_flag=True)
@click.version_option("0.1.0")
def cli(override):
    if override:
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

def main():
    cli()

if __name__ == '__main__':
    cli()