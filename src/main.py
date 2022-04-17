import click

@click.group()
@click.version_option("0.1.0")
def cli():
    """Layered Package Manager"""

@cli.command()
def sync():
    click.echo("Test!")

@cli.command()
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(name):
    click.echo(f"Hello {name}!")

def main():
    cli()

if __name__ == '__main__':
    cli()