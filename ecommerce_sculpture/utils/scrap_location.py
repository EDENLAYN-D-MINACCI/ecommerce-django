import requests, re, random
from bs4 import BeautifulSoup 


response = None
location = {}
headers_list = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows 
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]

#Pick a random browser headers
headers = random.choice(headers_list)
#Create a request session
r = requests.Session()
#Set request headers
r.headers = headers
#Request the page
response = r.get('https://www.showmyip.com/', headers=headers)
#print("\nUser-Agent Sent:%s\n\nHeaders Received by HTTPBin:"%(headers))
#print("-------------------")

soup = BeautifulSoup(response.content, 'html.parser', from_encoding="iso-8859-1")
rows = soup.find_all('td')
print(rows)


def get_item(my_list, index):
    try:
        index_element = cleanhtml(my_list[index + 1])
        print(index_element)
        return index_element
        
    except ValueError:
        print("item not found")
        return ""

def cleanhtml(raw_html):
  pattern = re.compile('<.*?>')
  return re.sub(pattern, '', str(raw_html))

def get_location():
    index = 0
    print(rows)

    for row in rows:

        if "Country" in row:
            location['country'] = get_item(rows, index)
        elif "Region" in row:
            location['region'] = get_item(rows, index)
        elif "City" in row:
            location['city'] = get_item(rows, index)
        elif "ZIP" in row:
            location['zip'] = get_item(rows, index)

        index += 1
        
    print(location)
    return location


if __name__ == '__main__':
    get_location()
