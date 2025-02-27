import requests

def query_asset_history(asset_code, start, end):
    headers = {
        'User-Agent': 'Mozilla/5.0 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.livecoinwatch.com/',
        'x-api-key': 'xxxxxxxxxxxxxxxxx',
        'Content-Type': 'application/json',
        'LCW-Version': '1',
        'LCW-Client': 'web',
        'Origin': 'https://www.livecoinwatch.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    json_data = {
        'currency': 'USD',
        'code': asset_code,
        'start': start,
        'end': end,
    }

    response = requests.post('https://api.livecoinwatch.com/coins/single/history', headers=headers, json=json_data)
    return response.text
