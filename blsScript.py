from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define email content
email = MIMEMultipart()
email['From'] = 'boundlesscuriosity237@gmail.com'
email['To'] = 'adityagoel237@gmail.com'
email['Subject'] = 'Test Email'
body = 'This is a test email sent from Python'
email.attach(MIMEText(body, 'plain'))


#configs for running headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# initialize the browser
browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

# navigate to the webpage with the dropdown
browser.get("https://www.blsindia-canada.com/appointmentbls/appointment.php")

# find the dropdown element
locationDropdown = Select(browser.find_element(By.ID, 'location'))
serviceTypeDropdown = Select(browser.find_element(By.ID, 'service_type'))
appDateTextField = browser.find_element(By.ID, 'app_date')

# select an option by visible text
locationDropdown.select_by_visible_text("Brampton")
serviceTypeDropdown.select_by_visible_text("Passport")

time.sleep(5)
appDateTextField.click()

for i in range(1,7):
  for j in range(1,8):
    xpath = "//html/body/div[5]/div[1]/table/tbody/tr[" + str(i) + "]" + "/td[" + str(j) +"]"
    dateClass = browser.find_element(By.XPATH, xpath)
    print(dateClass.get_attribute("class"))

    if (dateClass.get_attribute("class") == "new day activeClass"):
      print("FUCK YEAH")
      # Send email
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login('boundlesscuriosity237@gmail.com', 'yuiiulcvxxnnzblb')

      # server = smtplib.SMTP('localhost')
      text = email.as_string()
      server.sendmail('boundlesscuriosity237@gmail.com', 'adityagoel237@gmail.com', text)

      server.quit()

# while(True):
#   pass

browser.quit()
