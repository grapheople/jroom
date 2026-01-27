# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import os
import json

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
        remain_text = tds[7].get_text(" ", strip=True)
        etc_text = tds[9].get_text(" ", strip=True) if len(tds) >= 10 else ""

        total = _first_number(total_text) or 0
        remain = _first_number(remain_text) or 0

        subsidies.append({
            "locationName1": location_name1,
            "locationName2": location_name2,
            "totalCount": total,
            "applyCount": remain,
            "etc": etc_text,
        })

    return subsidies

if __name__ == "__main__":
    # tesla/electriccar.txt 파일에서 HTML 읽기
    # https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do
    # copy(document.getElementsByClassName('table01 ')[0].outerHTML)
    file_path = "source/electriccar.txt"
    
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일을 찾을 수 없습니다.")
        sample_html = "<ul></ul>" 
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            sample_html = f.read()

    # 상품 정보 파싱
    subsidyList = parse_subsidy(sample_html)

    out_path = os.path.join("json", f"electriccar_subside.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(subsidyList, ensure_ascii=False, indent=2))
