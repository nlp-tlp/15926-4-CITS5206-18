import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to ChromeDriver -need to be changed to the local chromedriver path
driver_path = "C:/Users/shanm/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

@pytest.fixture(scope="module")
def setup_browser():
    """Set up the Selenium WebDriver."""
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_navigation(setup_browser):
    """Test navigation through the Streamlit app."""
    driver = setup_browser
    # Open your Streamlit app (make sure it's running)
    driver.get("http://localhost:8501")  

    # Wait for the app to load
    #time.sleep(60)
    WebDriverWait(driver, 10).until(EC.title_contains("main"))

    # Test the initial page title
    assert "main" in driver.title  

    
def test_search_functionality(setup_browser):
    """Test the search functionality of the Streamlit app."""
    driver = setup_browser
    driver.get("http://localhost:8501")
    time.sleep(2)

    # Test the search bar functionality
    # Locate the input element by role 
    search_box = driver.find_element(By.CSS_SELECTOR, "input[role='combobox']")

    # Click on the input box to activate it 
    search_box.click()

    # Clear the input field (if needed)
    search_box.clear()

    # Populate the search box to VALVE
    search_box.send_keys("VALVE")
    time.sleep(1)  # Add slight delay to allow the dropdown to load

    # Wait for dropdown options to become visible
    dropdown_options = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li[role='option']"))
    )

    # Iterate through dropdown options and click 'VALVE'
    for option in dropdown_options:
        if option.text == "VALVE":  # Case-sensitive match
            option.click()
            break  # Exit the loop after clicking

    time.sleep(120)
        
    
