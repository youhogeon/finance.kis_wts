
from dataclasses import dataclass
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from kis_wts.actions.base import Action, ActionResult
from kis_wts.exception import KisWtsException
from kis_wts.kis_wts import KisWts


@dataclass
class LoginActionResult(ActionResult):
    name: str


class LoginAction(Action[LoginActionResult]):
    """브라우저인증서 로그인"""

    url_path = 'main/member/login/login.jsp'
    main_path = 'main/Main.jsp'
    
    def __init__(self, password: str):
        self.password = password

    def do(self, kis: KisWts) -> LoginActionResult:
        if kis.driver.current_url.endswith(self.main_path) and (name := self.is_logged_in(kis)):
            # 이미 로그인되어 있는 경우
            return LoginActionResult(name)

        try:
            kis.util.wait_and_click('#browerCert')
        except Exception:
            raise KisWtsException('보안 프로그램이 설치되어 있지 않습니다.')

        try:
            kis.util.wait_for_visible('div.pin_area')
            kis.util.press_keys(self.password)
        except Exception:
            raise KisWtsException('브라우저 인증서가 발급되어있지 않습니다.')

        if name := self.is_logged_in(kis):
            return LoginActionResult(name)
    
        raise KisWtsException('로그인에 실패했습니다.')

    def is_logged_in(self, kis: KisWts) -> Optional[str]:
        def wait_fn(driver: WebDriver):
            return driver.current_url.endswith(self.main_path)
        
        kis.util.wait(wait_fn)

        elem = kis.util.find_element('.my')

        return elem.text