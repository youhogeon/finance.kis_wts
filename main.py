from kis_wts.actions.debug import NoAction
from kis_wts.kis_wts import KisWts

wts = KisWts()

# (최초 실행 시) 브라우저인증서 발급, 보안프로그램 설치 등을 수동으로 진행해야 합니다.
wts.do(NoAction()) # 브라우저 띄우기
