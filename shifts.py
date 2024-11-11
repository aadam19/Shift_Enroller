from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

def login(driver):
    driver.get("https://pbwtool.kosta.ch")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_token")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    csrf_token_field = soup.find('input', {'name': '_token'})
    csrf_token = csrf_token_field['value'] if csrf_token_field else None

    if csrf_token:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.execute_script("document.getElementsByName('_token')[0].value = arguments[0];", csrf_token)
        driver.find_element(By.ID, "submit-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link[href='/helper/shifts']")))
        driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/helper/shifts']").click()
        WebDriverWait(driver, 10).until(EC.url_contains("helper/shifts"))
        return True
    else:
        print("Failed to retrieve CSRF Token.")
        return False

# Function to enroll in shifts
def enroll_in_shifts():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        if login(driver):
            shift_rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr.clickable-row"))
            )

            for index, shift in enumerate(shift_rows):
                try:
                    shift.click()
                    enroll_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".enroll-button-class"))  # Update with actual selector
                    )
                    enroll_button.click()
                    print(f"Enrolled in shift {index + 1}")
                    time.sleep(2)
                except Exception as e:
                    print(f"Could not enroll in shift {index + 1}")
                finally:
                    driver.back()
        else:
            print("Login failed; cannot enroll in shifts.")

    finally:
        driver.quit()


if __name__ == "__main__":
    enroll_in_shifts()