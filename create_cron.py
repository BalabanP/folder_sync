import os
import logging
from crontab import CronTab, CronSlices

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PYTHON_PATH = "python3"


def create_cron_file(**kwargs):
    with open(os.path.join(BASE_DIR, "cron_file.tab"), "w+"):
        file_cron = CronTab(tabfile=os.path.join(BASE_DIR, "cron_file.tab"))
    command = f"{PYTHON_PATH} files_manager.py " + f" ".join(
        map(lambda item: f"-{item[0]} {item[1]}", kwargs.items())
    )
    job = file_cron.new(command=command)
    if not CronSlices.is_valid(kwargs["sync_interval"]):
        logging.error("Incorect Chron time interval")
        raise Exception("Incorect Chron time interval")
    job.setall(kwargs["sync_interval"])
    file_cron.write()
