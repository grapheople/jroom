import asyncio
import subprocess
import os
from datetime import datetime
from make_news_json import make_news_json
from make_shop_json import make_shop_json
from make_subsidy_json import make_subsidy_json

async def main():
    """
    모든 JSON 생성 함수를 실행합니다.
    - make_news_json: 뉴스 데이터 생성
    - make_shop_json: 쇼핑 데이터 생성
    - make_subsidy_json: 전기차 보조금 데이터 생성
    - git add, commit, push 자동 실행
    """
    print("=" * 50)
    print("모든 JSON 파일 생성 시작")
    print("=" * 50)
    
    # 1. 뉴스 JSON 생성
    print("\n[1/3] 뉴스 JSON 생성 중...")
    try:
        make_news_json("테슬라")
        print("✓ 뉴스 JSON 생성 완료")
    except Exception as e:
        print(f"✗ 뉴스 JSON 생성 실패: {e}")
    
    # 2. 쇼핑 JSON 생성
    print("\n[2/3] 쇼핑 JSON 생성 중...")
    try:
        make_shop_json()
        print("✓ 쇼핑 JSON 생성 완료")
    except Exception as e:
        print(f"✗ 쇼핑 JSON 생성 실패: {e}")
    
    # 3. 전기차 보조금 JSON 생성 (비동기)
    print("\n[3/3] 전기차 보조금 JSON 생성 중...")
    try:
        await make_subsidy_json()
        print("✓ 전기차 보조금 JSON 생성 완료")
    except Exception as e:
        print(f"✗ 전기차 보조금 JSON 생성 실패: {e}")
    
    print("\n" + "=" * 50)
    print("모든 JSON 파일 생성 완료")
    print("=" * 50)
    
    # 4. Git 커밋 및 푸시
    print("\n[4/4] Git 커밋 및 푸시 중...")
    try:
        # 프로젝트 루트 디렉토리로 이동
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        os.chdir(project_root)

        # git pull
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("✓ git pull 완료")
        
        # git add
        subprocess.run(["git", "add", "json/"], check=True)
        print("✓ git add 완료")
        
        # git commit
        commit_message = f"Update JSON files - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"✓ git commit 완료: {commit_message}")
        
        # git push
        subprocess.run(["git", "push"], check=True)
        print("✓ git push 완료")
        
        print("\n" + "=" * 50)
        print("모든 작업 완료!")
        print("=" * 50)
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Git 작업 실패: {e}")
        print("(변경사항이 없거나 Git 설정을 확인해주세요)")
    except Exception as e:
        print(f"✗ Git 작업 중 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
