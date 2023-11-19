from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv,time

class Indeedjobs():
    def __init__(self) -> None:
        pass
    
    def header(self):
        header = ['Job Title','Job Url','Company Name','Comapny Location','Job Type','Salary','Responsibilities','Qualifaction Or Requries']
        with open(file="Indeed.csv",mode='w',newline='') as file:
            csv.writer(file).writerow(header)

    def userSearch(self):
        inputSearch = input('enter search about your job:- ')
        querry = '+'.join(inputSearch.split())
        return querry

    def openBrowser(self):
        driverPath = ChromeDriverManager().install()
        servc = Service(driverPath)
        driver = webdriver.Chrome(service=servc)
        return driver
    
    def getAndSaveLinks(self,driver,webUrl):
        driver.get(webUrl)
        time.sleep(4)
        urlTag = driver.find_elements(By.XPATH,'//h2[contains(@class,"jobTitle")]/a')
        for tag in urlTag:
            jobLink = tag.get_attribute('href')
            with open(file='jobsLinks.txt',mode='a') as file:
                file.write(jobLink + '\n')
    
    def readData(self):
        with open(file='jobsLinks.txt',mode='r') as file:
            readData = file.readlines()
            jobUrls = [data.strip() for data in readData]
            return jobUrls
    
    def parseData(self,driver,jobUrls):
        for url in jobUrls:
            driver.get(url)
            time.sleep(4)
            try: jobTitle = driver.find_element(By.XPATH,'//div[contains(@class,"jobsearch-JobInfoHeader-title")]/h1').text.strip()
            except: jobTitle = 'None'
            try: companyName = driver.find_element(By.XPATH,'//div[@data-company-name]/a').text.strip()
            except: companyName = 'None'
            try: comapnyLocation = driver.find_element(By.XPATH,'//div[contains(@data-testid,"companyLocation")]').text.strip()
            except: comapnyLocation = 'None'
            try: 
                jobTypeTag = driver.find_elements(By.XPATH,'//div[contains(text(),"Job Type")]/parent::div/div[2]//div[@class="css-tvvxwd ecydgvn1"]')
                jobType = ','.join([tag.get_attribute('textContent').strip() for tag in jobTypeTag])
            except: jobType = 'None'
            try: 
                salaryTag = driver.find_elements(By.XPATH,'//div[contains(text(),"Salary")]/parent::div/div[2]//div[@class="css-tvvxwd ecydgvn1"]')
                salary = ','.join([tag.get_attribute('textContent').strip() for tag in salaryTag])
            except: salary = 'None'
            try: 
                responsibilitiesTag = driver.find_elements(By.XPATH,'//div[@id="jobDescriptionText"]/ul[1]/li')
                responsibilities = '\n'.join([tag.get_attribute('textContent').strip() for tag in responsibilitiesTag])
            except: responsibilities = 'None'
            try: 
                qualifactaionOrRequriesTag = driver.find_elements(By.XPATH,'//div[@id="jobDescriptionText"]/ul[2]/li')
                qualifactionOrRequries = '\n'.join([tag.get_attribute('textContent').strip() for tag in qualifactaionOrRequriesTag])
            except: qualifactionOrRequries = 'None'
            row = [jobTitle,url,companyName,comapnyLocation,jobType,salary,responsibilities,qualifactionOrRequries]
            print(f"[Info] Getting Product:- {jobTitle}")
            self.saveData(row)
    
    def saveData(self,row):
        with open(file="Indeed.csv",mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)

    def run(self):
        querry = self.userSearch()
        driver = self.openBrowser()
        webUrl = f"https://pk.indeed.com/jobs?q={querry}"
        print(f"\n[Info] Getting Data from this urls:- \n")
        self.getAndSaveLinks(driver,webUrl)
        productUrls = self.readData()
        self.parseData(driver,productUrls)

open(file='jobsLinks.txt',mode='w').close()
myClass = Indeedjobs()
print(f"[Info] Do you want to delete all data and add new data! ")
answer = input('enter your decision (y/n):- ')
if answer == 'y':
    myClass.header()
    myClass.run()
else:
    myClass.run()

