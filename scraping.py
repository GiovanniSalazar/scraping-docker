import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
import json
import boto3
import uuid

companies_so = []

s3 = boto3.client('s3')
bucket ='scraping-indeed'

i = 1

while i <= 10 :
  #https://stackoverflow.com/jobs/companies?v=true&pg=3
  url = 'https://stackoverflow.com/jobs/companies?v=true&pg={}'.format(i)
  wd.get(url)
  result = wd.find_element_by_xpath("//div[@class='company-list']")
  companies = result.find_elements_by_xpath("div[@class='dismissable-company -company ps-relative js-dismiss-overlay-container p24 bb bc-black-3']")
  for x in companies:
    data = {}
    id_document = str(uuid.uuid4())
    name_company = x.find_element_by_xpath("div[@class='grid']//div[@class='grid--cell fl1 text']//h2[@class='fs-body2 mb4']//a").text
    link = x.find_element_by_xpath("div[@class='grid']//div[@class='grid--cell fl1 text']//h2[@class='fs-body2 mb4']//a").get_attribute('href')
    location = x.find_element_by_xpath("div[@class='grid']//div[@class='grid--cell fl1 text']//div[@class='grid gs12 gsx ff-row-wrap fs-body1']//div").text
    print(name_company)
    print(link)
    print(location)
    data.update({"name_company": name_company })
    data.update({"link": link })
    data.update({"location":location})

    uploadByteStream = bytes(json.dumps(data).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=id_document+'.json', Body=uploadByteStream)
    #print(location)
    # data.update({"name_company": name_company })
    # data.update({"link": link })
    # data.update({"location":location})
    # companies_so.append(data)

  i=i+1
