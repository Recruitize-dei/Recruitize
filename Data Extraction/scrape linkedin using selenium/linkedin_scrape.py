from selenium import webdriver
import selenium
import time
import os
import smtplib
import time
import datetime
from parsel import Selector
import pandas as pd
import numpy as np
import requests
import csv

##Reading csv file to extract links of profiles
with open('profile links.csv') as f:            ##profile links.csv in the same directory as that of program
    reader = csv.reader(f)
    links = np.array(list(reader)).flatten()

##Creaing output csv file
f=open('profile details.csv', 'a', newline='')
fieldnames = ['Name', 'Job Profile', 'Location', "College", "Degree", "Branch", "From Year","To Year", 'Profile Link']
writer = csv.DictWriter(f, fieldnames=fieldnames)
#writer.writeheader()

##Linkedin Login
e="gautam.shivam98@gmail.com"##add credentials here
p="shivam.123"##add credentials here
driver=webdriver.Chrome()
driver.maximize_window()
time.sleep(0.5)
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(1.5)
username=driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
time.sleep(1)
username.send_keys(e)
time.sleep(1)
password=driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
time.sleep(2)
password.send_keys(p)
time.sleep(1)
submit=driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button')
time.sleep(1.2)
submit.click()
print("Login Successful")
time.sleep(5)


##Function to check if data scraped is empty and remove extra spaces
def validate_field(field):
    if field==None:
       field = 'No results'
    return field.strip()

##Scrape Data from links extracted from csv file
for l in links[75:80]:
    driver.get(l)
    print("Scraping....", l)
    sel = Selector(text=driver.page_source)
    print("---------------------------------------------------------------------")
    name = validate_field(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first())
    print(name)
    job_profile = validate_field(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/div/h2/text()').extract_first())
    print(job_profile)
    location = validate_field(sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first())
    print(location)
    college = validate_field(sel.xpath('//*[@id="ember112"]/text()').extract_first())
    print(college)
    degree_name = validate_field(sel.xpath('//*[@id="ember354"]/span[1]/text()').extract_first())
    print(degree_name)
    branch = validate_field(sel.xpath('//*[@id="ember181"]/div[2]/div/p[2]/span[2]/text()').extract_first())
    print(branch)
    fromYear = validate_field(sel.xpath('//*[@id="ember181"]/div[2]/p/span[2]/time[1]/text()').extract_first())
    print(fromYear)
    toYear = validate_field(sel.xpath('//*[@id="ember181"]/div[2]/p/span[2]/time[2]/text()').extract_first())
    print(toYear)
    print("---------------------------------------------------------------------")
    try:
        writer.writerow({'Name': name, 'Job Profile': job_profile, 'Location': location, "College": college, "Degree": degree_name, "Branch": branch, "From Year": fromYear,"To Year": toYear,'Profile Link': l})
    except:
        print("Storing Data failed!! Kindly close the output csv file if it is open")
    try:
      more_button=driver.find_element_by_xpath('//*[@id="ember69"]')
      more_button.click()
      time.sleep(2)
      pdf_button=driver.find_element_by_xpath('//*[@id="ember78"]')
      pdf_button.click()
      time.sleep(10)##greater dealay for downloading PDF
      try:
          os.rename(r'C:\Users\BK GAUTAM\Downloads\Profile.pdf',r'C:\Users\BK GAUTAM\Downloads\\'+name+"_"+l+'.pdf')##change path   ##snippet not working
      except:
          print("Error Occured while renaming")
    except:
        print("Unable to download PDF")
    print("==================================================================")
## Closing browser and csv file
f.close()
driver.close()


print("Scraping Completed:)")
