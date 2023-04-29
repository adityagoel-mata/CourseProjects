import time
import smtplib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options 

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants
WEBDRIVER_BINARY_PATH = "/usr/bin/chromedriver"
APPOINTMENT_WEBPAGE_URL = "https://www.blsindia-canada.com/appointmentbls/appointment.php"
AVAILABLE_APPOINTMENT_CLASSNAME_1 = "day activeClass"
AVAILABLE_APPOINTMENT_CLASSNAME_2 = "new day activeClass"
AVAILABLE_APPOINTMENT_CLASSNAME_3 = "active day activeClass"
EMAIL_FROM = "goela19@mcmaster.ca"
APP_PASSWORD = "abcdefghijklm"
EMAIL_TO = "adityagoel237@gmail.com"
EMAIL_SUBJECT = "Appointment available"
EMAIL_BODY = "There is a slot available, book now!"

# Configs for a headless browser
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Functions

# Function to check availability of appointments:
def check_Appointments() -> bool:
	for week in range(1,7):				#Six rows for six weeks (Week[-1] + Week[1-4] + Week[+1]) is displayed
		for day in range(1,8):			#Seven days per week
			dateXPath = "//html/body/div[5]/div[1]/table/tbody/tr[" + str(week) + "]" + "/td[" + str(day) +"]"
			dateClass = browser.find_element(By.XPATH, dateXPath)
			print(dateClass.get_attribute("class"))

			if (dateClass.get_attribute("class") == AVAILABLE_APPOINTMENT_CLASSNAME_1
					or dateClass.get_attribute("class") == AVAILABLE_APPOINTMENT_CLASSNAME_2
					or dateClass.get_attribute("class") == AVAILABLE_APPOINTMENT_CLASSNAME_3):
				return True
	return False


# Function to email
def notify_Me() -> None:

    # Define email content
    email = MIMEMultipart()
    email['From'] = EMAIL_FROM
    email['To'] = EMAIL_TO
    email['Subject'] = EMAIL_SUBJECT
    body = EMAIL_BODY
    email.attach(MIMEText(body, 'plain'))

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_FROM, APP_PASSWORD)
    text = email.as_string()
    server.sendmail(EMAIL_FROM, EMAIL_TO, text)
    server.quit()


# Main Function
if __name__ == '__main__':
	
	# Initialize browser and open URL
	browser = webdriver.Chrome(WEBDRIVER_BINARY_PATH, options=chrome_options)
	browser.get(APPOINTMENT_WEBPAGE_URL)

	# Assign elements to variables
	locationDropdown = Select(browser.find_element(By.ID, 'location'))
	serviceTypeDropdown = Select(browser.find_element(By.ID, 'service_type'))
	appDateTextField = browser.find_element(By.ID, 'app_date')

	CITY_LIST = ["Brampton", "Toronto"]
	for city in CITY_LIST:
		locationDropdown.select_by_visible_text(city)
		serviceTypeDropdown.select_by_visible_text("Passport")
		time.sleep(5)
		appDateTextField.click()

		currentMonthStatus = check_Appointments()

		#Toggle to next month
		nextButtonXpath = "//html/body/div[5]/div[1]/table/thead/tr[1]/th[3]"
		nextButton = browser.find_element(By.XPATH, nextButtonXpath)
		nextButton.click()

		nextMonthStatus = check_Appointments()
		if(currentMonthStatus or nextMonthStatus):
			notify_Me()

	browser.quit()