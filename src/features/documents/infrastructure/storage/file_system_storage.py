from src.features.documents.infrastructure.storage.file_storage_interface import (
    FileStorage,
)
import pathlib
from typing import BinaryIO


class FileSystemStorage(FileStorage):
    def __init__(self):
        self._storage_folder = UPLOAD_DIR = (
            pathlib.Path(__name__).parent.parent.parent / "uploaded"
        )

        if not self._storage_folder.exists():
            pathlib.Path.mkdir(self._storage_folder)

    def upload(self, file: BinaryIO, filename: str):

        CHUNK_SIZE = 4
        file_location = pathlib.Path.joinpath(self._storage_folder, filename)

        with open(file_location, "wb") as f:
            while True:
                content = file.read(CHUNK_SIZE)

                if not content:
                    break

                f.write(content)

    def download(self, filename: str) -> pathlib.Path:
        file_location = pathlib.Path.joinpath(self._storage_folder, filename)

        if not file_location.exists():
            raise Exception("file does not exists")

        return file_location
