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
from driverpath import driver_path

@pytest.fixture(scope="module")
def setup_browser():
    """Set up the Selenium WebDriver."""
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get("http://localhost:8501")  # Open the Streamlit app
    yield driver
    driver.quit()

def wait_for_element(driver, by, value, timeout=20):
    """Helper function to wait for an element to be present."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element not found: {by}={value}")
        return None

def click_button_by_text(driver, button_text):
    """Helper function to click a button based on its text."""
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[.//p[text()='{button_text}']]"))
    )
    button.click()

def send_keys_to_element(driver, css_selector, keys):
    """Helper function to send keys to an input element."""
    element = wait_for_element(driver, By.CSS_SELECTOR, css_selector)
    element.click()
    element.clear()
    element.send_keys(keys)
    return element

def toggle_fullscreen(driver, iframe_tag_name):
    """Helper function to handle fullscreen and exit fullscreen."""
    iframe = driver.find_element(By.TAG_NAME, iframe_tag_name)
    driver.switch_to.frame(iframe)
    
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Go Fullscreen')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    button.click()
    time.sleep(2)
    driver.switch_to.default_content()

    try:
        driver.execute_script("if (document.fullscreenElement) { document.exitFullscreen(); }")
    except Exception as e:
        print(f"Error when using JavaScript to exit fullscreen: {str(e)}")

def test_page_load(setup_browser):
    """Test navigation through the Streamlit app."""
    driver = setup_browser
    WebDriverWait(driver, 10).until(EC.title_contains("main"))
    assert "main" in driver.title  

def test_search_functionality(setup_browser):
    """Test the search functionality."""
    driver = setup_browser
    search_box = send_keys_to_element(driver, "input[aria-autocomplete='list']", "VALVE")
    
    dropdown_options = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li[role='option']"))
    )
    
    for option in dropdown_options:
        if option.text == "VALVE":
            option.click()
            break

    time.sleep(1)

    # Test number input functionality
    for input_id, expected_value in [("number_input_1", "4"), ("number_input_2", "5")]:
        number_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, input_id))
        )
        number_input.click()
        number_input.send_keys(Keys.BACKSPACE * 3)
        number_input.send_keys(expected_value)
        number_input.send_keys(Keys.TAB)
        time.sleep(1)
        assert number_input.get_attribute("value") == expected_value, f"Number input {input_id} did not update correctly!"

def test_fullscreen_buttons(setup_browser):
    """Test the navigation buttons for switching between plots."""
    driver = setup_browser

    # Switch to Network Plot
    click_button_by_text(driver, "NETWORK Plot")
    time.sleep(70)
    toggle_fullscreen(driver, 'iframe')

    # Switch to Tree Plot
    click_button_by_text(driver, "TREE Plot")
    time.sleep(60)
    toggle_fullscreen(driver, 'iframe')

def test_node_click(setup_browser):
    """Test clicking on a specific node in the D3 plot."""
    driver = setup_browser
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    script = """
    const d3Container = document.querySelector("#d3-container svg");
    if (!d3Container) return null;
    const textElements = d3Container.querySelectorAll("text");
    let circleClicked = false;

    textElements.forEach((element) => {
        const titleElement = element.querySelector('title');
        const textContent = titleElement ? titleElement.textContent.trim() : element.textContent.trim();

        if (textContent === 'VALVE') {
            const parentG = element.closest('g');
            const circleElement = parentG.querySelector('circle');
            if (circleElement) {
                circleElement.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                circleClicked = true;
            }
        }
    });
    return circleClicked;
    """
    circle_clicked = driver.execute_script(script)
    assert circle_clicked, "Circle associated with 'VALVE' was not clicked."
    driver.switch_to.default_content()
    time.sleep(10)

def test_level_adjustment(setup_browser):
    """Test adjusting the levels of Superclass and Subclass."""
    driver = setup_browser
    time.sleep(1)

    superclass_input = driver.find_elements(By.XPATH, "//input[@aria-label='Number of Levels of Superclass']")
    subclass_input = driver.find_elements(By.XPATH, "//input[@aria-label='Number of Levels of Subclass']")

    assert len(superclass_input) > 0, "Superclass level input not found"
    assert len(subclass_input) > 0, "Subclass level input not found"

    print("Level adjustment inputs found successfully")

def test_chart_type_switching(setup_browser):
    """Test switching between Tree Plot and Network Plot."""
    driver = setup_browser
    buttons = driver.find_elements(By.TAG_NAME, "button")
    button_texts = [button.text for button in buttons]
    
    tree_plot_exists = any("TREE Plot" in text for text in button_texts)
    network_plot_exists = any("NETWORK Plot" in text for text in button_texts)
    
    assert tree_plot_exists, "Tree Plot button not found"
    assert network_plot_exists, "Network Plot button not found"

def test_search_history(setup_browser):
    """Test the search history functionality."""
    driver = setup_browser
    time.sleep(5) 
    
    search_box = wait_for_element(driver, By.CSS_SELECTOR, "input[aria-autocomplete='list']")
    if search_box:
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        search_box.send_keys("accumulator")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        search_box.click()
        search_box.clear()
        search_box.click()
        search_box.send_keys("pipe")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        history_items = wait_for_element(driver, By.XPATH, "//div[contains(., 'Recent Searches:')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", history_items)
        time.sleep(5)
        assert history_items, "Search history not found"
    else:
        pytest.fail("Search box not found")

def test_documentation_toggle(setup_browser):
    """Test expanding and collapsing the documentation section."""
    driver = setup_browser
    summary_element = wait_for_element(driver, By.TAG_NAME, "summary")
    time.sleep(1)
    summary_element.click()  # Expand
    time.sleep(1)
    summary_element.click()  # Collapse
