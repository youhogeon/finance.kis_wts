# 한국투자증권 WTS 자동화

## 사전 준비 사항
* Google Chrome 설치
* 한국투자증권 보안프로그램(필수 프로그램 限) 설치
* 한국투자증권 브라우저인증서 발급
    * `브라우저인증서 발급 방법` 섹션 참고

## 지원하는 Action
* 로그인
    * 브라우저 인증서 로그인
* 계좌이체
    * 보유 계좌간 이체

## 예제
### 브라우저 인증서 로그인
```python
wts = KisWts()

login_action = LoginAction(CONFIG.browser_cert_pw)
result = wts.do(login_action)

print(f"Logged in as: {result.name}")
```

### 보유 계좌간 이체
```python
result = wts.do(
    TransferAction(
        source_account="67818474-21",
        target_account="67818474-01", # '커피 한 잔 마시고싶다..' 라고 생각만 해보는 중 :)
        amount="ALL",
        account_pw="0000",
        browser_cert_pw="000000",
    )
)

print(f"Transferred {result.amount} with fee {result.fee}. Remaining balance: {result.balance}")
```

## 비고
### 브라우저 인증서 발급 방법
1. 기 발급된 브라우저 인증서를 사용하는 방법
    * 브라우저 인증서가 발급된 `Google Chrome`의 User Data 경로를 지정하세요.
    * User Data는 `%appdata%\..\Local\Google\Chrome\User Data` 등에 위치합니다.
    * `wts = KisWts(userdata_path="...")`
1. 브라우저 인증서를 새로 발급하는 방법
    * User Data가 없는 깨끗한 상태의 브라우저에서 새 인증서를 발급하세요.
    * 아래 코드를 통해 브라우저를 실행할 수 있습니다.
        ```python
        wts = KisWts()
        wts.do(NoAction()) # 브라우저 띄우기
        ```