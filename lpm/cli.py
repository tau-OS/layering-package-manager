import click
from rich.console import Console
from lpm.commands.search import command_search
from lpm.commands.info import command_info
from lpm.commands.install import command_install
from lpm.commands.remove import command_remove
from lpm.commands.update import command_update
from lpm.commands.groups.info import command_group_info
from lpm.commands.groups.install import command_group_install
from lpm.commands.groups.remove import command_group_remove
from lpm.commands.groups.search import command_group_search
from lpm.commands.groups.update import command_group_update
from lpm import dnf as dnf_utils
import dnf

from lpm.utils import make_sync

console = Console()
error_console = Console(stderr=True, style="bold red")


@click.group()
@click.option("--override", help="Perform transaction on the base layer", is_flag=True)
@click.option(
    "--disablerepo",
    help="Temporarily disable active repositories for the purpose of the current lpm command.",
    multiple=True,
    metavar="<repo>",
)
@click.version_option("0.1.0")
def cli(override, disablerepo):
    """Layered Package Manager"""
    dnf_utils.setup_handlers()

    if override:
        # TODO this should be able to be disabled with something like --override=true
        console.print(
            "[bold red]WARNING![/bold red] The [italic]--override[/italic] flag makes changes to your base system.",
            style="bold",
        )
        console.print("Only use this option if you know what you're doing!")
        click.confirm("Do you understand?", abort=True)

        click.echo("Using base layer")

    if disablerepo:
        for repo in disablerepo:
            repos = dnf.base.repos.get_matching(repo)
            if repos == []:
                error_console.print(f"Repo [italic]{repo}[/italic] not found")
                exit()
            repos.disable()
        console.print(
            f"Repos Disabled: {','.join([str(i) for i in disablerepo])}",
            style="bold red",
        )

    # THIS MUST BE LAST
    dnf_utils.base.fill_sack()
    dnf_utils.base.read_comps()


@cli.command()
@click.argument("packages", nargs=-1, required=True)
@make_sync
async def install(packages):
    """Overlay additional packages"""
    await command_install(packages)


@cli.command()
@click.argument("package")
def remove(package):
    """Remove overlayed packages"""
    command_remove(package)


@cli.command()
@click.argument("keyword")
def search(keyword):
    """Search package details for the given string"""
    command_search(keyword)


@cli.command()
@click.argument("package")
def info(package):
    """Display details about a package or group of packages"""
    command_info(package)


@cli.command()
def rollback():
    """Revert to the previously booted tree.\n
    With the override flag, this resets the base layer"""
    click.echo("Test")


@cli.command()
@click.argument("package", required=False)
def update(package):
    """Upgrade a single package or all the packages on your system"""
    command_update(package)


@cli.group()
def groups():
    """Manage groups"""


@groups.command()
@click.argument("group")
def install(group):
    """Overlay group"""
    command_group_install(group)


@groups.command()
@click.argument("group")
def remove(group):
    """Remove overlayed groups"""
    command_group_remove(group)


@groups.command()
@click.argument("keyword")
def search(keyword):
    """Search groups for the given string"""
    command_group_search(keyword)


@groups.command()
@click.argument("group")
def info(group):
    """Display details about a group"""
    command_group_info(group)


@groups.command()
@click.argument("group")
def update(group):
    """Upgrade a single group"""
    command_group_update(group)
