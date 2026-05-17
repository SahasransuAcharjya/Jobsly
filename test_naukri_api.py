import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "appid": "109",
    "systemid": "naukri",
    "clientid": "d3js"
}
url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=python&pageNo=1"
response = requests.get(url, headers=headers)
print("Status:", response.status_code)
if response.status_code == 200:
    data = response.json()
    jobs = data.get("jobDetails", [])
    print("Found jobs:", len(jobs))
    if jobs:
        print("First job title:", jobs[0].get("title"))
else:
    print("Response text:", response.text[:200])
