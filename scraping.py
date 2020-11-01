import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
import json
import boto3
import uuid
import datetime
# Using selenium web driver to scrap the web
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
wd_description = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

# boto3 to connect this script with s3 when this upload the data to bucket
s3 = boto3.client('s3')
bucket ='scraping-indeed'

# I will save the file name with this name value "date"
now = datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
date = '{}-{}-{}'.format(year, month, day)

# Just to test this script I will go just for 10 page using a simple while to scrap each pagination
i = 10
while i < 100 :
  url = 'https://ca.indeed.com/jobs?q={}&fromage={}&sort={}&start=60'.format('python sql','1','date',i)
  # Scraping web DOM elements html
  wd.get(url)
  result = wd.find_elements_by_xpath("//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")
  for x in result:
    try:
      # Find and parse elements DOM
      job = x.find_element_by_xpath("h2[@class='title']//a").text
      link = x.find_element_by_xpath("h2[@class='title']//a").get_attribute("href")
      location = x.find_element_by_class_name('location.accessible-contrast-color-location').text
      company = x.find_element_by_class_name('company').text
      wd_description.get(link)
      description = wd_description.find_element_by_id("jobDescriptionText").text
      # building the json file
      data = {}
      id_document = str(uuid.uuid4())
      data.update({"id_document": id_document })
      data.update({"job": job })
      data.update({"link": link })
      data.update({"location":location})
      data.update({"company":company})
      data.update({"description":description})
      uploadByteStream = bytes(json.dumps(data).encode('UTF-8'))
      # saving file json on s3 bucket
      s3.put_object(Bucket=bucket, Key=id_document+'.json', Body=uploadByteStream)
    except Exception as e:
      print(e)
      pass

  i=i+10
