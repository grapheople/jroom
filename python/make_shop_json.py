import requests
import csv
import json
import io
import urllib.parse

def fetch_gsheet_as_json(sheet_url):
    """
    Fetches a Google Spreadsheet as CSV and converts it to a list of dictionaries.
    The first row of the sheet is used as field names.
    """
    # Parse the URL and remove fragment
    parsed_url = urllib.parse.urlparse(sheet_url)
    query = urllib.parse.parse_qs(parsed_url.query)
    
    # Get gid if present
    gid = query.get('gid', ['0'])[0]
    
    # Construct export URL
    # Replace /edit... with /export
    path_parts = parsed_url.path.split('/')
    if 'edit' in path_parts:
        edit_idx = path_parts.index('edit')
        path_parts = path_parts[:edit_idx] + ['export']
    
    new_path = '/'.join(path_parts)
    export_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        new_path,
        '',
        f'format=csv&gid={gid}',
        ''
    ))

    print(f"Debug: Exporting from {export_url}")
    
    response = requests.get(export_url)
    response.raise_for_status()
    
    # Use response.content.decode('utf-8') to handle BOM and ensure correct decoding
    content = response.content.decode('utf-8-sig')
    
    # Use io.StringIO with the decoded content. 
    # The csv module in Python 3 handles universal newlines if we don't specify them in StringIO,
    # but for csv.reader, we often want to ensure it sees the whole thing.
    f = io.StringIO(content)
    reader = csv.DictReader(f)
    
    data = []
    for row in reader:
        # Clean up keys and values if needed (e.g. stripping whitespace)
        clean_row = {k.strip(): v for k, v in row.items() if k is not None}
        data.append(clean_row)
    
    return data

def main():
    keyword = "tesla"
    test_url = "https://docs.google.com/spreadsheets/d/1Zocy2KfOAA0UlPmCmci0SIq-cKGf8mXGBpHhKa5UWRA/edit?gid=0#gid=0"
    
    try:
        print(f"Goal: Fetch data from Google Sheet and convert to JSON")
        json_data = fetch_gsheet_as_json(test_url)
        
        # Optionally save to file
        out_path = os.path.join("json", f"{fileNameMap[keyword]}_shop.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # Print a snippet
        if json_data:
            print("\nFirst row preview:")
            print(json.dumps(json_data[0], ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
