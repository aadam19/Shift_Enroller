import time, os
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from shifts import enroll_in_shifts

load_dotenv()

# Path to the chromedriver
CHROME_DRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# Function to get the page content hash
def get_shifts_page_hash():
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get("https://pbwtool.kosta.ch/helper/shifts")
    time.sleep(2)  # Allow page to fully load

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
    
    while True:
        time.sleep(5)  # Check every 5 minutes (adjust as needed)
        
        try:
            current_hash = get_shifts_page_hash()
            
            # Check if the page content has changed
            if current_hash != last_hash:
                print("Change detected! Attempting to enroll in shifts...")
                enroll_in_shifts()
                last_hash = current_hash  # Update the hash after successful enrollment
            else:
                print("No change detected.")
                
        except Exception as e:
            print(f"Error during monitoring: {e}")

# Start monitoring
monitor_shifts()
