import click

@click.command()
@click.option('--name', prompt='Your name',
              help='The person to greet.')
@click.version_option("0.1.0")

def hello(count, name):
    """Layered Package Manager"""
    click.echo(f"Hello {name}!")

def main():
    hello()

if __name__ == '__main__':
    hello()