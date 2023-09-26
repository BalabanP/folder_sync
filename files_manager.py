import os
import shutil
import argparse
from create_cron import create_cron_file, logging, BASE_DIR


SYNC_INTERVAL = "5 * * * *"


class FilesManager:
    def __init__(self) -> None:
        self.args = self._create_arguments()
        self._create_cron_file()

    def sinchronize(self):
        if not os.path.exists(self.args.source_folder_path):
            os.makedirs(self.args.source_folder_path)
        if not os.path.exists(self.args.replica_folder_path):
            os.makedirs(self.args.replica_folder_path)
        origin_files = set(os.listdir((self.args.source_folder_path)))
        replica_files = set(os.listdir((self.args.replica_folder_path)))
        files_ori_rep = origin_files - replica_files
        files_rep_ori = replica_files - origin_files
        if files_ori_rep:
            self._copy(files_ori_rep)
            logging.info(
                f"The files:{list(files_ori_rep)} was copied to replica folder"
            )
        elif files_rep_ori:
            self._delete(files_rep_ori)
            logging.info(
                f"The files:{list(files_rep_ori)} was deleted from replica folder"
            )
        else:
            logging.info("There is no files to sync")

    def _create_cron_file(self):
        create_cron_file(**vars(self.args))

    def _create_arguments(self):
        parser = argparse.ArgumentParser(
            prog="Folder Replication",
            description="replicate the content of folder in replica",
            epilog="please provide the arguments",
        )
        parser.add_argument(
            "-sync",
            "--sync_interval",
            default=SYNC_INTERVAL,
            type=str,
            help="Please specify a valid crontab interval",
        )
        parser.add_argument(
            "-s",
            "--source_folder_path",
            default=os.path.join(BASE_DIR, "origin"),
            type=str,
            help="provide origin folder path",
        )
        parser.add_argument(
            "-r",
            "--replica_folder_path",
            default=os.path.join(BASE_DIR, "replica"),
            type=str,
            help="provide replica folder path",
        )
        return parser.parse_args()

    def _copy(self, files):
        [
            shutil.copy(
                os.path.join(self.args.source_folder_path, i),
                os.path.join(self.args.replica_folder_path, i),
            )
            for i in files
        ]

    def _delete(self, files):
        [os.remove(os.path.join(self.args.replica_folder_path, i)) for i in files]


if __name__ == "__main__":
    file_manager = FilesManager()
    try:
        file_manager.sinchronize()
    except Exception as e:
        logging.error(f"There is an error on script:{__name__}:{e}")
        raise Exception(f"There is an error on script:{__name__}:{e}")
