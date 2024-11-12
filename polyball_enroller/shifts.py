from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, os, hashlib
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
            print("Successfully logged in. Enrolling in shifts...")
            shift_rows = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr.clickable-row"))
            )
            len_shifts = len(shift_rows)
            print(f"Found {len_shifts} shifts to enroll in.")

            curr = 0
            while curr < len_shifts:
                shift_rows = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr.clickable-row"))
                )

                shift = shift_rows[curr]
                print(f"Enrolling in shift {curr + 1}...")
                try:
                    shift.click()

                    print("Shift clicked")
                    
                    # Locate and click the enroll button within the modal
                    enroll_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[wire\\:click='startEnrolling']"))
                    )
                    enroll_button.click()

                    # Add a short delay for modal animation
                    time.sleep(1) 

                    # Wait for the confirmation modal and the "Confirm" button to be visible
                    confirm_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[wire\\:click='confirmEnrolling']"))
                    )
                    print(confirm_button)
                    confirm_button.click()

                    # Click the "Back to shifts" link to return to the shift list
                    back_to_shifts_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.no-underline.text-gray-500"))
                    )
                    back_to_shifts_link.click()
                    time.sleep(1)  # Wait briefly for the page to refresh

                    print(f"Enrolled in shift {curr + 1}")

                except Exception as e:
                    print(f"Could not enroll in shift {curr + 1}")
                    
                    # Click the "Back to shifts" link to return to the shift list
                    back_to_shifts_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.no-underline.text-gray-500"))
                    )
                    back_to_shifts_link.click()
                    time.sleep(1)  # Wait briefly for the page to refresh
                
                curr += 1
        else:
            print("Login failed; cannot enroll in shifts.")

        print("Enrollment process completed.")

    finally:
        print("Closing the browser...")
        driver.quit()

def get_shifts_page_hash():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    try:
        if not login(driver):
            print("Login failed; cannot get page hash.")
            return None
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    shifts_table = soup.find("tbody")  # Update selector if needed
    page_content = shifts_table.get_text() if shifts_table else ""
    
    driver.quit()
    
    # Calculate a hash of the content
    return hashlib.md5(page_content.encode('utf-8')).hexdigest()

# Main monitoring function
def monitor_shifts():
    print("Starting shifts monitor...")
    
    last_hash = get_shifts_page_hash()
    print("Initial hash:", last_hash)
    
    while True:
        time.sleep(15)  # Check every 5 minutes (adjust as needed)
        
        try:
            current_hash = get_shifts_page_hash()
            print("Current hash:", current_hash)
            
            # Check if the page content has changed
            if current_hash != last_hash:
                print("Change detected! Attempting to enroll in shifts...")
                enroll_in_shifts()
                last_hash = current_hash  # Update the hash after successful enrollment
            else:
                print("No change detected.")
                
        except Exception as e:
            print(f"Error during monitoring: {e}")

if __name__ == "__main__":
    monitor_shifts()