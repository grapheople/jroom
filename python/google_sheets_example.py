import gspread
from google.oauth2.service_account import Credentials

# 1. 인증 설정 (credentials.json 파일이 루트 디렉토리에 있어야 합니다)
# Google Cloud Console에서 발급받은 서비스 계정 키 파일 이름입니다.
SERVICE_ACCOUNT_FILE = 'googleApiKey.json'

# 사용할 권한(Scope) 설정
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def append_data_to_sheet(sheet_name, data_row):
    """
    구글 스프레드시트에 한 줄의 데이터를 추가합니다.
    
    :param sheet_name: 스프레드시트 이름
    :param data_row: 추가할 데이터 리스트 (예: ['2024-01-27', '상품명', 10000])
    """
    try:
        # 서비스 계정 인증
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)

        # 스프레드시트 열기 (이름으로 열기)
        # 주의: 스프레드시트가 서비스 계정 이메일과 공유되어 있어야 합니다.
        sheet = client.open(sheet_name).get_worksheet(0) # 첫 번째 워크시트 선택

        # 데이터 추가 (마지막 행 다음에 추가)
        sheet.append_row(data_row)
        
        print(f"데이터 삽입 성공: {data_row}")

    except Exception as e:
        print(f"오류 발생: {e}")
        print("\n[알림] 오류가 발생했다면 다음 사항을 확인하세요:")
        print(f"1. {SERVICE_ACCOUNT_FILE} 파일이 스크립트와 같은 경로에 있는지 확인")
        print("2. 구글 스프레드시트가 '서비스 계정 이메일'에 '편집자' 권한으로 공유되어 있는지 확인")
        print("3. Google Sheets API와 Google Drive API가 활성화되어 있는지 확인")

if __name__ == "__main__":
    target_sheet_name = "쿠팡파트너스 상품리스팅" # 실제 스프레드시트 이름으로 변경
    new_data = ["2024-01-27", "테스트 상품", "15,000원", "비고"]
    
    print(f"'{target_sheet_name}' 시트에 데이터를 삽입합니다...")
    append_data_to_sheet(target_sheet_name, new_data)
