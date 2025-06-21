
import time
from dataclasses import dataclass
from typing import Literal, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from kis_wts.actions.base import Action, ActionResult
from kis_wts.exception import KisWtsException
from kis_wts.kis_wts import KisWts
from kis_wts.util.string import extract_num


@dataclass
class TransferActionResult(ActionResult):
    amount: int
    fee: int
    balance: int

class TransferAction(Action[TransferActionResult]):
    """보유 계좌 간 이체"""

    url_path = 'main/banking/opentransfer/NTransfer.jsp'
    
    def __init__(
        self,
        *,
        source_account: str,
        target_account: str,
        amount: Union[int, Literal['ALL']],
        account_pw: str,
        browser_cert_pw: str,
    ):
        self.source_account = source_account
        self.target_account = target_account
        self.amount = str(amount)
        
        self.account_pw = account_pw
        self.browser_cert_pw = browser_cert_pw

    def do(self, kis: KisWts) -> TransferActionResult:
        time.sleep(5)

        ## Modal 있는 경우 닫기 (`이용PC지정 서비스 신청안내` 등)
        try:
            kis.util.wait_and_click('.modal .btn_close')
        except Exception:
            ...
        
        ## 출금 계좌 선택
        select_el_accounts = kis.util.find_element('#IBCOM_ACCOUNT')
        select_el_accounts = kis.util.find_parent(select_el_accounts)
        select_el_accounts.click()

        a_el_accounts = select_el_accounts.find_elements(By.TAG_NAME, "a")
        time.sleep(1) # wait for animation

        for el in a_el_accounts:
            val = el.get_attribute("innerHTML")
            if val and val.startswith(self.source_account):
                kis.util.wait_and_click(el)

                break
        else:
            raise KisWtsException(f"출금 계좌 '{self.source_account}'을(를) 찾을 수 없습니다.")

        kis.util.find_element('#IBCOM_S_I_AC_PWD').send_keys(self.account_pw)
        kis.util.find_element('#IBCOM_S_I_AC_PWD').send_keys(Keys.TAB)

        kis.util.wait_for_visible('#js-amtCont')
        balance = extract_num(kis.util.find_element("#js-IBCOM_S_O_PAYMENT").text)

        if self.amount == 'ALL':
            self.amount = str(balance)
        elif int(self.amount) > int(balance):
            raise KisWtsException(f"출금가능금액이 부족합니다. 출금가능금액: {balance}원, 이체 금액: {self.amount}원")
        
        if self.amount == '0':
            raise KisWtsException("거래금액은 1원 이상이어야 합니다.")

        ## 입금 계좌 선택
        box = kis.util.wait_for_visible('#js-transferTabCont .tab_button')
        a_el_accounts = box.find_elements(By.TAG_NAME, "a")
        for el in a_el_accounts:
            val = el.get_attribute("innerText")
            if val == "직접입력":
                kis.util.wait_and_click(el)

                break
        else:
            raise KisWtsException("입금 계좌 선택 탭을 찾을 수 없습니다.")
    
        kis.util.wait_and_click('.js-mybank')
        options = kis.util.find_elements('#bankingAccount span')
        for opt in options:
            val = opt.get_attribute("innerText")
            if val == self.target_account:
                kis.util.wait_and_click(kis.util.find_parent(opt))

                break
        else:
            raise KisWtsException(f"입금 계좌 '{self.target_account}'을(를) 찾을 수 없습니다.")

        ## 금액 입력 및 이체
        kis.util.find_element('.fe_Amount2').send_keys(self.amount, Keys.TAB)
        kis.util.wait_and_click('#goNext')

        def check_iframe(driver: WebDriver):
            iframe_els = driver.find_elements(By.TAG_NAME, 'iframe')
            for iframe_el in iframe_els:
                if iframe_el.accessible_name == '이체 내용확인 프레임':
                    return iframe_el
            
            return False
        
        try:
            iframe_el = kis.util.wait(check_iframe)
        except Exception:
            raise KisWtsException("이체 내용 확인 프레임을 찾을 수 없습니다.")

        kis.driver.switch_to.frame(iframe_el)
        kis.driver.execute_script("fSubmit_Before();")
        # kis.util.wait_and_click("#Btn_fSubmit_Before")

        kis.util.wait_for_visible('div.pin_area')
        kis.util.press_keys(self.browser_cert_pw)

        kis.driver.switch_to.default_content()

        ## 이체 결과 확인
        def check_result(driver: WebDriver):
            if "실행완료" not in driver.title:
                return False

            els = driver.find_elements(By.CLASS_NAME, 'h2_title')
            for el in els:
                if el.text == '출금계좌 정보':
                    return el
            
            return False

        try:
            result_el = kis.util.wait(check_result)
        except Exception:
            raise KisWtsException("이체 결과를 찾을 수 없습니다.")

        box_el = kis.util.find_parent(kis.util.find_parent(result_el))
        tr_el = box_el.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(1)')

        amount = extract_num(tr_el.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text)
        fee = extract_num(box_el.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span').text)
        balance = extract_num(box_el.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span').text)

        return TransferActionResult(amount, fee, balance)