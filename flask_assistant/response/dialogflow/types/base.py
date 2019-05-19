
import abc


class BaseSerializer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass
