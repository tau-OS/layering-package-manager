import dnf
from lpm.handlers.progress import ProgressMetre

base = dnf.Base()
base.read_all_repos()

def setup_handlers():
    for repo in base.repos.iter_enabled():
        repo.set_progress_bar(ProgressMetre())