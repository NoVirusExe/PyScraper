from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from manage_data import queue

class Progress_Bar:

    def __init__(self):
        self.progress = Progress(
            TextColumn("[white]Scanning URLs"),
            BarColumn(complete_style="white", finished_style="white"),
            TextColumn("{task.completed} scanned"),
            TimeElapsedColumn()
        )
        self.task = None

    def __enter__(self):
        self.progress.start()
        self.task = self.progress.add_task("scan", total=queue.qsize())
        return self

    def __exit__(self, exc_type, exc, tb):
        self.progress.stop()

    def advance(self, n=1):
        self.progress.update(self.task, advance=n)