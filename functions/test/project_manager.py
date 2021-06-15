import subprocess  # nosec

import config
from google.cloud import firestore


class ProjectManager:
    def __init__(self):
        self.db = firestore.Client()

    def send_message(self, message):
        subprocess.run(
            [
                "gcloud",
                "functions",
                "call",
                config.FUNCTION_TO_MESSAGE,
                "--region",
                config.REGION,
                "--data",
                message,
            ]
        )  # nosec

    def clean_project(self):
        return NotImplemented
