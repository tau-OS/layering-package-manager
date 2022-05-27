import dnf
from rich.progress import Progress, SpinnerColumn, DownloadColumn, TransferSpeedColumn
from rich.console import Console

# TODO this really really needs to use rich.progress
# https://dnf.readthedocs.io/en/latest/api_callback.html
# https://rich.readthedocs.io/en/latest/progress.html

console = Console()


class ProgressMetre(dnf.callback.DownloadProgress):
    """Multi-file download progess metre"""

    progress_bar = Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        DownloadColumn(),
        TransferSpeedColumn(),
    )

    def __init__(self):
        self.total_files = 0
        self.total_size = 0
        self.total_drpm = 0
        self.tasks = {}
        self.download_size = {}

        self.done_size = 0
        self.done_files = 0

    def start(self, total_files, total_size, total_drpms=0):
        self.total_files = total_files
        self.total_size = total_size
        self.total_drpm = total_drpms
        self.tasks = {}
        self.download_size = {}

        self.progress_bar.__enter__()
        self.progress_bar.start()

    def progress(self, payload, done):
        name = payload.__str__()
        if payload.download_size != 0:
            self.download_size[name] = payload.download_size

        payload_size = self.download_size.get(name, 0)

        if not name in self.tasks:
            self.tasks[name] = self.progress_bar.add_task(name, total=payload_size)

        self.progress_bar.update(self.tasks[name], completed=done, total=payload_size)

    def end(self, payload, status, err_msg):
        payload_size = self.download_size.get(payload.__str__(), 0)

        if self.progress_bar.finished == True:
            self.progress_bar.stop()
            self.progress_bar.__exit__(None, None, None)

        if err_msg:
            console.print(f"{err_msg}")

        self.progress_bar.update(
            self.tasks[payload.__str__()],
            completed=payload_size,
            total=payload_size,
        )
