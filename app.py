import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import csv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to log in to Kaggle
def log_in(username, password):
    try:
        # Locate the "Sign in with Email" button and click it
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Sign in with Email']]"))
        )
        sign_in_button.click()

        # Enter email and password
        username_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        # Locate the "Sign In" button and click it
        sign_in_button = driver.find_element(By.XPATH, "//button[.//span[text()='Sign In']]")
        sign_in_button.click()

        try:
            # Check for invalid credentials message
            invalid_credentials = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='site-content']/div[2]/div[1]/div/div[1]/div/div/div/div/div/p"))
            ).text
            
            if "incorrect" in invalid_credentials:
                logging.error("The username or password provided is incorrect.")
                driver.quit()
                exit()
        except:
            logging.info("Login successful")

        driver.implicitly_wait(5)
    except Exception as e:
        logging.error(f"Error during login: {e}")
        driver.quit()
        exit()

# Function to fetch element by their xpath
def fetch_element(xpath, default=None):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).text
    except:
        return default

# Function to append data scraped from the web to a list
def append_data_scrap_from_web(list_items, start, total_count):
    for index in range(start, len(list_items)):
        try:
            if total_count > threshold:
                return total_count, index
            
            # Wait for all list items to be present
            list_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'MuiListItem-root MuiListItem-gutters MuiListItem-divider sc-drMgrp dllDGS css-iicyhe')]"))
            )

            # Click on the current list item link
            link = list_items[index].find_element(By.XPATH, ".//a")
            driver.execute_script("arguments[0].click();", link)

            # extract data
            competition_name = fetch_element("//*[@id='site-content']/div[2]/div/div/div[2]/div[2]/div[1]/h1")
            competition_host = fetch_element("//*[@id='site-content']/div[2]/div/div/div[6]/div[4]/div/div[1]/div[1]/p")
            prizes = fetch_element("//*[@id='site-content']/div[2]/div/div/div[6]/div[4]/div/div[2]/div/div/p[1]")
            participation = fetch_element("//*[@id='site-content']/div[2]/div/div/div[6]/div[4]/div/div[3]/div/p[1]")

            try:
                description = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "description"))
                ).text
            except:
                description = None

            # Append data to the list
            all_data.append([competition_name, competition_host, prizes, participation, description])

            # Navigate back to competitions page
            driver.back()

            # Re-click "All Competitions" button if necessary
            if total_count < 19:
                all_competitions_button = driver.find_element(By.XPATH, "//button[.//div[.//span[text()='All Competitions']]]")
                driver.execute_script("arguments[0].click();", all_competitions_button)
                time.sleep(5)

            total_count += 1
        except Exception as e:
            logging.error(f"Error processing list item {index}: {e}")
            return total_count, index
    return total_count, len(list_items)

# Set up the Chrome driver using webdriver-manager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Navigate to Kaggle login page
driver.get("https://www.kaggle.com/account/login")

# Load environment variables from .env file
load_dotenv()
# Get credentials from environment variables
username = os.getenv('USER-NAME')
password = os.getenv('PASSWORD')
threshold = int(os.getenv('THRESHOLD'))
log_in(username, password)

try:
    # Navigate to competitions page
    competitions_link = driver.find_element(By.XPATH, "//li[.//p[text()='Competitions']]")
    competitions_link.click()
    driver.implicitly_wait(5)

    # Click "All Competitions" button
    all_competitions_button = driver.find_element(By.XPATH, "//button[.//div[.//span[text()='All Competitions']]]")
    driver.execute_script("arguments[0].click();", all_competitions_button)
    driver.implicitly_wait(5)

    total_count = 0
    all_data = []

    # Loop until the threshold is met
    while total_count < threshold:
        try:
            # Wait for all list items to be present
            list_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'MuiListItem-root MuiListItem-gutters MuiListItem-divider sc-drMgrp dllDGS css-iicyhe')]"))
            )

            length = len(list_items)
            start = 0
            
            while True:
                total_count, start = append_data_scrap_from_web(list_items, start, total_count)
                if (start < length) and (total_count <= threshold):
                    list_items = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'MuiListItem-root MuiListItem-gutters MuiListItem-divider sc-drMgrp dllDGS css-iicyhe')]"))
                    )
                    total_count, start = append_data_scrap_from_web(list_items, start, total_count)
                else:
                    break
            
            # Click next page button
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@title='Next Page' and @aria-label='Next Page']"))
            )
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(5)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            break

    # Write the extracted data to a CSV file
    with open('competition_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Competition Name', 'Competition Host', 'Prizes', 'Participation', 'Description'])
        writer.writerows(all_data)

    logging.info("Data has been written to competition_details.csv")
finally:
    driver.quit()
