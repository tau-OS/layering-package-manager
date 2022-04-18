import dnf

# TODO this really really needs to use rich.progress
class ProgressMetre(dnf.callback.DownloadProgress):
    """Multi-file download progess metre"""

    def __init__(self):
        self.total_files = 0
        self.total_size = 0
        self.total_drpm = 0

    def start(self, total_files, total_size, total_drpms=0):
        self.total_files = total_files
        self.total_size = total_size
        self.total_drpm = total_drpms

    def progress(self, payload, done):
        total = self.total_size - int(payload.download_size)
        print(f"Downloading {payload}: {total} out of {int(done)}")

    def end(self, payload, status, err_msg):
        print(f"Downloading {payload} finished")

        print(status)

        print(err_msg)