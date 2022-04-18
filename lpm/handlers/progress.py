import dnf
from rich.progress import Progress, SpinnerColumn, DownloadColumn, TransferSpeedColumn

# TODO this really really needs to use rich.progress
# https://dnf.readthedocs.io/en/latest/api_callback.html
# https://rich.readthedocs.io/en/latest/progress.html

progress = Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    DownloadColumn(),
    TransferSpeedColumn(),
)
progress.__enter__()


class ProgressMetre(dnf.callback.DownloadProgress):
    """Multi-file download progess metre"""

    def __init__(self):
        self.total_files = 0
        self.total_size = 0
        self.total_drpm = 0
        self.tasks = {}
        self.download_size = {}

    def start(self, total_files, total_size, total_drpms=0):
        self.total_files = total_files
        self.total_size = total_size
        self.total_drpm = total_drpms
        self.tasks = {}
        self.download_size = {}

    def progress(self, payload, done):
        name = payload.__str__()
        if payload.download_size != 0:
            self.download_size[name] = payload.download_size

        payload_size = self.download_size.get(name, 0)

        if not name in self.tasks:
            self.tasks[name] = progress.add_task(name, total=payload_size)

        progress.update(self.tasks[name], completed=done, total=payload_size)

    def end(self, payload, status, err_msg):
        payload_size = self.download_size.get(payload.__str__(), 0)
        progress.update(
            self.tasks[payload.__str__()],
            completed=payload_size,
            total=payload_size,
        )
