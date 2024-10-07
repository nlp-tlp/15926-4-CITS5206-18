import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

# Path to ChromeDriver -need to be changed to the local chromedriver path
driver_path = "/Users/imac/Downloads/chromedriver-mac-x64/chromedriver"

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
        
def wait_for_element(driver, by, value, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element not found: {by}={value}")
        return None

def test_comparative_view(setup_browser):
    """Test enabling the comparative view."""
    driver = setup_browser
    driver.get("http://localhost:8501")
    time.sleep(10) 
    
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

    if len(select_boxes) >= 2:
        for select_box in select_boxes[:2]: 
            select_box.click()
            time.sleep(1) 
            option = wait_for_element(driver, By.XPATH, "//div[@role='option'][1]")  
            if option:
                option.click()
            time.sleep(1) 

def test_search_history(setup_browser):
    """Test the search history functionality."""
    driver = setup_browser
    driver.get("http://localhost:8501")
    time.sleep(10) 
    
    search_box = wait_for_element(driver, By.CSS_SELECTOR, "input[aria-autocomplete='list']")
    if search_box:
        search_box.send_keys("VALVE")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        search_box.clear()
        search_box.send_keys("PIPE")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        history_items = wait_for_element(driver, By.XPATH, "//div[contains(., 'Recent Searches:')]")
        assert history_items, "Search history not found"
    else:
        pytest.fail("Search box not found")

def test_chart_type_switching(setup_browser):
    """Test switching between Tree Plot and Network Plot."""
    driver = setup_browser
    driver.get("http://localhost:8501")
    time.sleep(10)  

    buttons = driver.find_elements(By.TAG_NAME, "button")
    button_texts = [button.text for button in buttons]
    print("Available buttons:", button_texts)

    tree_plot_exists = any("TREE Plot" in text for text in button_texts)
    network_plot_exists = any("NETWORK Plot" in text for text in button_texts)

    assert tree_plot_exists, "Tree Plot button not found"
    assert network_plot_exists, "Network Plot button not found"

    time.sleep(5) 
    page_source = driver.page_source
    tree_container_exists = "d3-container" in page_source
    network_container_exists = "networkx-container" in page_source

    assert tree_container_exists or network_container_exists, "Neither Tree Plot nor Network Plot container was found"

    print("Chart switching test passed successfully")

def test_level_adjustment(setup_browser):
    driver = setup_browser
    driver.get("http://localhost:8501")
    time.sleep(10)

    superclass_input = driver.find_elements(By.XPATH, "//input[@aria-label='Number of Levels of Superclass']")
    subclass_input = driver.find_elements(By.XPATH, "//input[@aria-label='Number of Levels of Subclass']")

    assert len(superclass_input) > 0, "Superclass level input not found"
    assert len(subclass_input) > 0, "Subclass level input not found"

    print("Level adjustment inputs found successfully")