import argparse
import json
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "googleApiKey.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def load_worksheet(sheet_url, worksheet_index=0):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(sheet_url)
    return spreadsheet.get_worksheet(worksheet_index)


def sheet_to_records(sheet):
    headers = sheet[0]

    # 유효한 헤더 컬럼만 유지
    valid_cols = [
        i for i, h in enumerate(headers)
        if isinstance(h, str) and h.strip() != ""
    ]

    # name 컬럼 인덱스 찾기
    try:
        required_idx = headers.index("name")
    except ValueError:
        raise ValueError(f"'name' 컬럼이 헤더에 없습니다")

    result = []

    for row in sheet[1:]:
        # name 값이 없으면 행 전체 스킵
        if required_idx >= len(row):
            continue

        name_val = row[required_idx]
        if not isinstance(name_val, str) or name_val.strip() == "":
            continue

        obj = {}
        for i in valid_cols:
            if i >= len(row):
                continue

            val = row[i]
            if val is None:
                continue
            if isinstance(val, str) and val.strip() == "":
                continue

            obj[headers[i]] = val

        if obj:
            result.append(obj)

    result.sort(key=lambda x: x["order"], reverse=True)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Read a Google Sheet where the first column is field names."
    )
    parser.add_argument(
        "--worksheet-index",
        type=int,
        default=0,
        help="Worksheet index (0-based). Default: 0",
    )
    args = parser.parse_args()

    worksheet = load_worksheet("https://docs.google.com/spreadsheets/d/1Zocy2KfOAA0UlPmCmci0SIq-cKGf8mXGBpHhKa5UWRA/edit?gid=0#gid=0", args.worksheet_index)
    values = worksheet.get_all_values()
    records = sheet_to_records(values)

    output_path = Path(__file__).resolve().parents[1] / "json" / "tesla_products.json"
    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
