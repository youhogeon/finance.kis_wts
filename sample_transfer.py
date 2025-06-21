import os
import sys

from config import CONFIG
from kis_wts.actions.login import LoginAction
from kis_wts.actions.transfer import TransferAction
from kis_wts.kis_wts import KisWts

if __name__ == "__main__":
    # 명령줄 인자 파싱
    if len(sys.argv) != 4:
        print(f"Usage: python {os.path.basename(__file__)} <source_account> <target_account> <amount>")
        
        sys.exit(1)

    source_account, target_account, amount = sys.argv[1:4]
    amount = int(amount) if amount != 'ALL' else 'ALL'

    # 로그인 및 계좌이체
    wts = KisWts()
    result = wts.do(LoginAction(CONFIG.browser_cert_pw))

    print(f"Logged in as: {result.name}")

    result = wts.do(
        TransferAction(
            source_account=source_account,
            target_account=target_account,
            amount=amount,
            account_pw=CONFIG.account_pw,
            browser_cert_pw=CONFIG.browser_cert_pw,
        )
    )

    print(f"Transferred {result.amount} with fee {result.fee}. Remaining balance: {result.balance}")