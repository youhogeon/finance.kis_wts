

import time

from kis_wts.actions.base import Action, ActionResult
from kis_wts.kis_wts import KisWts


class NoActionResult(ActionResult):
    ...


class NoAction(Action[NoActionResult]):
    """아무 동작도 하지 않는 액션
    
    디버깅, 브라우저인증서 발급 등의 목적으로 사용,
    """

    url_path = 'main/Main.jsp'
    
    def __init__(self, delay: int = 3600):
        self.delay = delay

    def do(self, kis: KisWts) -> NoActionResult:
        time.sleep(self.delay)

        return NoActionResult()