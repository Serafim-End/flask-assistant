
from typing import Optional, Any, List

import abc


class TypesInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def card(self, title: str,
             subtitle: Optional[str] = None,
             img_url: Optional[str] = None,
             buttons: Optional[Any] = None) -> 'TypesInterface':
        pass

    @abc.abstractmethod
    def quick_replies(self, replies: List[str],
                      title: Optional[str] = None) -> 'TypesInterface':
        pass

    @abc.abstractmethod
    def link_out(self, name: str, url: str) -> 'TypesInterface':
        pass


class AskInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ask(self, **kwargs):
        pass


class TellInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def tell(self, **kwargs):
        pass


class EventInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def event(self,  event: str, **kwargs) -> None:
        pass


class PermissionInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def permission(self, permissions: List[str],
                   context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:
        pass


class ListInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_item(self, title: str,
                  key: Optional[str] = None,
                  synonyms: Optional[List[str]] = None,
                  description: Optional[str] = None,
                  image: Optional[Any] = None) -> None:
        pass

    @abc.abstractmethod
    def list(self, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def carousel(self, **kwargs) -> None:
        pass
