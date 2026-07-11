from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def upload(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def download(self, *args, **kwargs):
        raise NotImplementedError()
