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


def sheet_to_records(values):
    if not values:
        return []

    max_cols = max(len(row) for row in values)
    records = []

    for col in range(1, max_cols):
        record = {}
        for row in values:
            if not row:
                continue
            key = row[0].strip() if len(row) > 0 else ""
            if not key:
                continue
            value = row[col] if len(row) > col else ""
            record[key] = value
        if any(value != "" for value in record.values()):
            records.append(record)

    return records


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

    output_path = Path(__file__).resolve().parents[1] / "json" / "tesla_products_out.json"
    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
