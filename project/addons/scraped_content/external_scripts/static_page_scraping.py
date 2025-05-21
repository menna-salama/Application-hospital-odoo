import requests
from bs4 import BeautifulSoup
import json

url = "https://venturebeat.com/about/"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    page_title = soup.title.string.strip() if soup.title else "No Title Found"

    content_elements = soup.find_all(["p", "h1", "h2", "h3"])
    page_content = "\n".join(
        [element.get_text(strip=True) for element in content_elements]
    )

    data = {"title": page_title, "content": page_content, "url": url}

    with open("venturebeat_about.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Save data to  venturebeat_about.json")
else:
    print(f"Error: {response.status_code}")
