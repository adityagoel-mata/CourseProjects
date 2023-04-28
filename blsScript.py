import time
import smtplib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options 

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configs for a headless browser
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize browser and open URL
browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
browser.get("https://www.blsindia-canada.com/appointmentbls/appointment.php")

# Assign useful elements to variables
locationDropdown = Select(browser.find_element(By.ID, 'location'))
serviceTypeDropdown = Select(browser.find_element(By.ID, 'service_type'))
appDateTextField = browser.find_element(By.ID, 'app_date')


# Operations Structure
def performOperations(blsOffice):
    locationDropdown.select_by_visible_text(blsOffice)
    serviceTypeDropdown.select_by_visible_text("Passport")
    time.sleep(5)
    appDateTextField.click()
    checkAppointments()

    #Check appointments in the next month
    nextButtonXpath = "//html/body/div[5]/div[1]/table/thead/tr[1]/th[3]"
    nextButton = browser.find_element(By.XPATH, nextButtonXpath)
    nextButton.click()
    checkAppointments()


# Functions

# Function to check availability of appointments:
def checkAppointments():
  for i in range(1,7):        #Six rows for six weeks (Week[-1] + Week[1-4] + Week[+1]) is displayed
    for j in range(1,8):      # Seven days pwer week    
      dateXPath = "//html/body/div[5]/div[1]/table/tbody/tr[" + str(i) + "]" + "/td[" + str(j) +"]"
      dateClass = browser.find_element(By.XPATH, dateXPath)
      print(dateClass.get_attribute("class"))

      if (dateClass.get_attribute("class") == "new day activeClass"):
        notifyMe()

# Function to email
def notifyMe():
    # Define email content
    email = MIMEMultipart()
    email['From'] = 'goela19@mcmaster.ca'
    email['To'] = 'adityagoel237@gmail.com'
    email['Subject'] = 'Test Email'
    body = 'There is an appointment available'
    email.attach(MIMEText(body, 'plain'))

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('goela19@mcmaster.ca', '<password>')
    text = email.as_string()
    server.sendmail('goela19@mcmaster.ca', 'adityagoel237@gmail.com', text)

    server.quit()


# Main Function
performOperations("Brampton")
performOperations("Toronto")

browser.quit()
