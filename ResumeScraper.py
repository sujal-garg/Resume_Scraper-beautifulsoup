import requests
from bs4 import BeautifulSoup
import csv
import time


url = "https://www.postjobfree.com/resumes?q=title%3A%28python+developer%29&l=india&radius=25"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
title_tags = soup.find_all('h3', attrs={'class': 'itemTitle'})
links = ["https://www.postjobfree.com" + title_tag.a['href'] for title_tag in title_tags]
results = []
for link in links:
    res = requests.get(link)
    print(res.status_code, link)
    content = BeautifulSoup(res.content, 'html.parser')
    results.append({
        'job_title': content.find('div', attrs={'class': 'leftColumn'}).find('h1').get_text(),
        'resume': content.find('div', attrs={'class': 'normalText'}).get_text()[:-23]
    })
    time.sleep(3)
with open('resumes.csv', 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
    writer.writeheader()
    for row in results:
        writer.writerow(row)
