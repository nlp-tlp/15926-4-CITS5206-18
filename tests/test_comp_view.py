import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from driverpath import driver_path

@pytest.fixture(scope="module")
def setup_browser():
    """Set up the Selenium WebDriver."""
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    # Open the Streamlit app (make sure it's running)
    driver.get("http://localhost:8501")  

    yield driver
    driver.quit()

def test_pageLoad(setup_browser):
    """Test navigation through the Streamlit app."""
    driver = setup_browser
    # Wait for the app to load
    WebDriverWait(driver, 10).until(EC.title_contains("main"))

    # Test the initial page title
    assert "main" in driver.title  

def wait_for_element(driver, by, value, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element not found: {by}={value}")
        return None

def select_node(driver, label, value):
    """
    Helper function to select a node from the listbox and verify the selected value.
    
    :param driver: The WebDriver instance.
    :param label: The aria-label used to locate the listbox (e.g., 'Select First Node' or 'Select Second Node').
    :param value: The value to be selected (e.g., 'FLUID ACCUMULATOR').
    """
    # Locate the listbox by its aria-label
    listbox = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"div[data-baseweb='select'] input[aria-autocomplete='list'][aria-label*='{label}']"))
    )

    # Click on the listbox to open the dropdown
    listbox.click()
    time.sleep(5)

    # Clear the existing value in the listbox
    listbox.clear()

    # Send the new value to the listbox
    listbox.send_keys(value)

    # Press ENTER to confirm the selection
    listbox.send_keys(Keys.ENTER)

    # Locate the div that displays the selected value
    selected_value_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{value}')]"))
    )

    # Verify that the correct value was selected
    assert selected_value_div.text == value, f"Expected '{value}', but got {selected_value_div.text}"


def test_comparative_view(setup_browser):
    """Test enabling the comparative view and selecting nodes."""
    driver = setup_browser
    time.sleep(10)

    # Enable comparative view
    comparative_checkbox = wait_for_element(driver, By.XPATH, "//label[contains(., 'Enable Comparative View')]//input")
    if comparative_checkbox:
        driver.execute_script("arguments[0].click();", comparative_checkbox)
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@data-baseweb, 'select')]"))
        )

        select_boxes = driver.find_elements(By.XPATH, "//div[contains(@data-baseweb, 'select')]")
        assert len(select_boxes) >= 2, "Not enough select boxes found for comparative view"
    else:
        pytest.fail("Comparative view checkbox not found")

    # Select the first node
    select_node(driver, "Select First Node", "FLUID ACCUMULATOR")

    # Select the second node
    select_node(driver, "Select Second Node", "PISTON ACCUMULATOR")

    # Select First Plot Type
    select_node(driver, "Select First Plot Type", "D3.js Plot")

    # Select Second Plot Type
    select_node(driver, "Select Second Plot Type", "NetworkX Plot")

    time.sleep(10)

    # Disable comparative view at the end by clicking the checkbox again
    if comparative_checkbox:
        driver.execute_script("arguments[0].click();", comparative_checkbox)
        time.sleep(5)
    else:
        pytest.fail("Comparative view checkbox not found")
