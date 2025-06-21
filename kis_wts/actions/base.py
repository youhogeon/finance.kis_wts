from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from kis_wts.constant import Constants

if TYPE_CHECKING:
    from kis_wts.kis_wts import KisWts

__all__ = ['Action', 'ActionResult']


class ActionResult:
    ...

T = TypeVar('T', bound='ActionResult', covariant=True)

class Action(ABC, Generic[T]):
    url_path: Optional[str] = None

    @abstractmethod
    def do(self, kis: 'KisWts') -> T:
        ...
    
    @property
    def url(self) -> Optional[str]:
        if self.url_path is None:
            return None
        
        return f'{Constants.host.rstrip('/')}/{self.url_path.lstrip('/')}'
