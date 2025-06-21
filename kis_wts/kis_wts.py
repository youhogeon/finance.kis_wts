import os
from typing import Optional, TypeVar

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from kis_wts.actions.base import Action, ActionResult
from kis_wts.util.webdriver import WebDriverUtil

T = TypeVar('T', bound='ActionResult')


class KisWts:
    def __init__(
        self,
        userdata_path: Optional[str] = None, # 절대경로
    ):
        self.userdata_path = userdata_path or os.path.join(os.getcwd(), 'userdata')

        opt = webdriver.ChromeOptions()
        opt.add_argument(f"--user-data-dir={self.userdata_path}")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
        self.util = WebDriverUtil(self.driver)

    def do(self, action: Action[T]) -> T:
        if action.url:
            self.load_url(action.url)

        return action.do(self)
    
    def load_url(self, url: str) -> None:
        self.driver.get(url)
        self.util.wait(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading")))