# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import os
import json
import asyncio
from playwright.async_api import async_playwright

def _first_number(text):
	# Extract the first number-like token, allowing commas.
	match = re.search(r'\d[\d,]*', text)
	if not match:
	    return None
	return int(match.group().replace(',', ''))

def parse_subsidy(html_content):
    """
    table HTML의 tbody 영역을 파싱하여 JSON 문자열을 반환합니다.
    - 1번째 td: locationName1
    - 2번째 td: locationName2
    - 6번째 td: 첫 번째 숫자 -> totalCount
    - 8번째 td: 첫 번째 숫자 -> applyCount
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tbody = soup.find('tbody') or soup
    subsidies = []

    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 8:
            continue

        location_name1 = tds[0].get_text(strip=True)
        location_name2 = tds[1].get_text(strip=True)
        total_text = tds[5].get_text(" ", strip=True)
        recieved_text = tds[6].get_text(" ", strip=True)
        release_text = tds[7].get_text(" ", strip=True)
        remain_text = tds[8].get_text(" ", strip=True)
        etc_text = tds[9].get_text(" ", strip=True) if len(tds) >= 10 else ""

        total = _first_number(total_text) or 0
        recieved = _first_number(recieved_text) or 0
        release = _first_number(release_text) or 0
        remain = _first_number(remain_text) or 0

        subsidies.append({
            "locationName1": location_name1,
            "locationName2": location_name2,
            "totalCount": total,
            "recievedCount": recieved,
            "releaseCount": release,
            "remainCount": remain,
            "etc": etc_text,
        })

    return subsidies

async def make_subsidy_json():
    async with async_playwright() as p:
        # 브라우저 실행
        browser = await p.chromium.launch(headless=True)
        # User-Agent 설정
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("전기차 보조금 페이지 접속 중...")
        url = "https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do"
        
        try:
            # 페이지 이동
            await page.goto(url, wait_until="networkidle", timeout=60000)

            # table01 클래스를 가진 테이블이 로드될 때까지 대기
            print("테이블 데이터 대기 중...")
            await page.wait_for_selector(".contentList", timeout=30000)

            # 테이블 데이터 추출
            contentList = await page.query_selector(".contentList")
            
           

            # HTML 소스 저장 (백업용)
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            source_dir = os.path.join(project_root, "source")
            os.makedirs(source_dir, exist_ok=True)
            
            file_path = os.path.join(source_dir, "ev_subsidy_source.txt")
            table = await contentList.inner_html()
            
            subsidyList = parse_subsidy(table)

            out_path = os.path.join("json", f"electriccar_subside.json")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(subsidyList, ensure_ascii=False, indent=2))

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(make_subsidy_json())
    

