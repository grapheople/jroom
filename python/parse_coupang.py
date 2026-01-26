import json
import os
from bs4 import BeautifulSoup

def parse_coupang_html(file_path, output_json_path):
    """
    coupang.txt의 HTML 태그에서 상품 정보를 추출하여 JSON 파일로 저장합니다.
    """
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일이 존재하지 않습니다.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    products = []

    # 각 상품 아이템(product-item)을 순회합니다.
    product_items = soup.find_all('div', class_='product-item')

    for item in product_items:
        product = {}

        # 1. 상품명 (LinesEllipsis 클래스 내의 텍스트)
        desc_div = item.find('div', class_='product-description')
        if desc_div:
            # <wbr> 태그나 다른 태그들을 무시하고 텍스트만 추출
            product['name'] = desc_div.get_text(strip=True).replace('…', '').replace('…', '')
        
        # 2. 이미지 URL
        img_tag = item.find('img', alt='product')
        if img_tag and 'src' in img_tag.attrs:
            product['thumb'] = img_tag['src']

        # 3. 가격 정보 (할인율, 원래 가격, 판매 가격)
        price_div = item.find('div', class_='product-price')
        if price_div:            
            # 판매 가격
            sale_price = price_div.find('div', class_='sale-price')
            if sale_price:
                # 배송 방식 뱃지 확인 (로켓배송 등)
                delivery_badge = sale_price.find('span', class_='delivery-badge')
                if delivery_badge:
                    product['delivery_type'] = "Rocket" # 뱃지가 있으면 로켓배송 등으로 간주
                
                # 순수 가격 텍스트만 추출
                sale_price_label = sale_price.find('span', class_='currency-label')
                product['price'] = sale_price_label.get_text(strip=True) if sale_price_label else ""

        if product:
            products.append(product)

    # 결과를 JSON 파일로 저장
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print(f"성공: {len(products)}개의 상품 정보를 {output_json_path}에 저장했습니다.")
    return products

if __name__ == "__main__":
    keyword = "tesla"
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_file = os.path.join(project_root, "source", f"{keyword}_coupang.txt")
    output_file = os.path.join(project_root, "json", f"{keyword}_products.json")
    
    parse_coupang_html(input_file, output_file)
