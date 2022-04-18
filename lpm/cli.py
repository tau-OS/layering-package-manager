import click
from rich.console import Console
from lpm.commands.search import command_search
from lpm import dnf

console = Console()
error_console = Console(stderr=True, style="bold red")

@click.group()
@click.option('--override', help="Perform transaction on the base layer", is_flag=True)
@click.option('--disablerepo', help="Temporarily disable active repositories for the purpose of the current lpm command.", multiple=True)
@click.version_option("0.1.0")
def cli(override, disablerepo):
    """Layered Package Manager"""
    if override:
        # TODO this should be able to be disabled with something like --override=true
        console.print("[bold red]WARNING![/bold red] The [italic]--override[/italic] flag makes changes to your base system." , style="bold")
        console.print("Only use this option if you know what you're doing!")
        click.confirm('Do you understand?', abort=True)

        click.echo("Using base layer")

    if disablerepo:
        for repo in disablerepo:
            repos = dnf.base.repos.get_matching(repo)
            if repos == []:
                error_console.print(f"Repo [italic]{repo}[/italic] not found")
                exit()
            repos.disable()
        console.print(f"Repos Disabled: {','.join([str(i) for i in disablerepo])}", style="bold red")

    # THIS MUST BE LAST
    dnf.base.fill_sack()

@cli.command()
def install():
    """Overlay additional packages"""
    click.echo("Test!")

@cli.command()
def remove():
    """Remove overlayed packages"""
    click.echo("Test!")

@cli.command()
@click.argument('keyword')
def search(keyword):
    """Search package details for the given string"""
    command_search(keyword)

@cli.command()
def info():
    """Display details about a package or group of packages"""
    click.echo("Test!")

@cli.command()
def rollback():
    """Revert to the previously booted tree.\n
    With the override flag, this resets the base layer"""
    click.echo("Test")