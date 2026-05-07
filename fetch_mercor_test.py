import requests
import json
import re

response = requests.get('https://work.mercor.com/explore')
match = re.search(r'__NEXT_DATA__.*?>(.*?)</script>', response.text)
if match:
    data = json.loads(match.group(1))
    print("Keys in pageProps:", data.get("props", {}).get("pageProps", {}).keys())
    
    # Save the whole JSON to see it
    with open('mercor_test.json', 'w') as f:
        json.dump(data, f)
    print("Saved to mercor_test.json")
else:
    print("Could not find NEXT_DATA")
