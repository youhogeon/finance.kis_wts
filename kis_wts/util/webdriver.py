from typing import Any, Tuple, Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebDriverUtil:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait(self, ec: Any, timeout: int = 60):
        wait = WebDriverWait(self.driver, timeout)

        return wait.until(ec)

    def wait_for_visible(self, mark: Union[Tuple[str, str], str], timeout: int = 60):
        wait = WebDriverWait(self.driver, timeout)

        if isinstance(mark, str):
            mark = (By.CSS_SELECTOR, mark)

        return wait.until(EC.visibility_of_element_located(mark))

    def wait_for_present(self, mark: Union[Tuple[str, str], str], timeout: int = 60):
        wait = WebDriverWait(self.driver, timeout)

        if isinstance(mark, str):
            mark = (By.CSS_SELECTOR, mark)

        return wait.until(EC.presence_of_element_located(mark))

    def wait_and_click(self, mark: Union[WebElement, Tuple[str, str], str], timeout: int = 60):
        wait = WebDriverWait(self.driver, 60)

        if isinstance(mark, str):
            mark = (By.CSS_SELECTOR, mark)

        elem = wait.until(EC.element_to_be_clickable(mark))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        ActionChains(self.driver).move_to_element(elem).click(elem).perform()

        return elem
    
    def press_keys(self, keys: str, pause: float = 0.5):
        ac = ActionChains(self.driver)
        for ch in keys:
            ac.send_keys(ch).pause(pause)
        
        ac.send_keys(Keys.NULL)
        ac.perform()
    
    def find_element(self, css_selector: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def find_elements(self, css_selector: str) -> list[WebElement]:
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
    
    def find_parent(self, elem: WebElement) -> WebElement:
        return elem.find_element(By.XPATH, '..')