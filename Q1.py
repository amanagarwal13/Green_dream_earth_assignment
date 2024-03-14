import os
import csv
import requests
from bs4 import BeautifulSoup
from lxml import html
import re

url='https://www.lse.ac.uk/study-at-lse/undergraduate/degree-programmes-2024/ba-history#:~:text=BA%20History%20at%20LSE%20is,world%20we%20live%20in%20today.'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tree = html.fromstring(response.content)
    
    # Extracting degree type
    li_element = soup.find('li', class_='keyDetails__item--grad')
    degree_type = li_element.text.strip()

    # Extracting application deadline
    application_deadline = soup.find_all('td')[1].text
    
    # Extracting duration
    duration = soup.find_all('td')[2].text

    # Extracting tuition fee
    elements_fee = tree.xpath('//*[@id="form1"]/div[3]/div/div[2]/section/div/section[4]/div/div/p[5]')
    for element in elements_fee:
        text_content = element.text.strip()
        pattern = r'£(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)'
        matches = re.search(pattern, text_content)
        tuition_fee = "£"+matches.group(1)

    # Extracting description
    description = tree.xpath('//*[@id="form1"]/div[3]/div/div[2]/div/p[1]')
    for element in description:
        description_brief = element.text.strip()

    # Extracting requirements
    requirements_elements = tree.xpath('//*[@id="form1"]/div[3]/div/div[2]/section/div/section[2]/div/div/p[position() >= 2 and position() <= 6] | //*[@id="form1"]/div[3]/div/div[2]/section/div/section[2]/div/div/ul')
    requirements = '\n'.join([element.text_content().strip() for element in requirements_elements])

    # Storing data in CSV
    with open('degree_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree Type', 'Application Deadline', 'Duration', 'Tuition Fee', 'Description', 'Requirements'])
        writer.writerow([degree_type, application_deadline, duration, tuition_fee, description_brief, requirements])
else:
    print(f"Failed to fetch the page: {url}")
