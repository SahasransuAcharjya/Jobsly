import requests
from bs4 import BeautifulSoup

URL = "https://www.naukri.com/python-developer-jobs-in-bangalore"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
job_cards = soup.select(".srp-jobtuple-wrapper, #listContainer > div[class*='job-listing-container'] > div > div")
for card in job_cards:
    title_elem = card.select_one("a.title")
    if not title_elem or not title_elem.get_text(strip=True):
        continue
    
    title = title_elem.get_text(strip=True)
    link = title_elem.get("href")
    
    comp_elem = card.select_one("a.comp-name")
    company = comp_elem.get_text(strip=True) if comp_elem else None
    
    loc_elem = card.select_one(".locWdth")
    location = loc_elem.get_text(strip=True) if loc_elem else None
    
    print({
        "title": title,
        "company": company,
        "location": location,
        "link": link
    })