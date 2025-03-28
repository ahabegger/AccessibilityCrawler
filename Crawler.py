# Python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def login(username, password, elevance):
    chrome_options = Options()
    # Uncomment to run in headless mode if needed:
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    standard_login_url = "https://www.mobilehealthconsumer.com/weba/#/auth/login"
    elevance_login_url = "https://angulartest.mobilehealthconsumer.com/"

    if not elevance:
        login_url = standard_login_url
        driver.get(login_url)

        wait = WebDriverWait(driver, 20)
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[contains(.,'Log in')]")
        login_button.click()

        # Wait until redirect from login page
        wait.until(lambda d: "auth/login" not in d.current_url)
        time.sleep(20)  # Extend wait if Angular takes longer

        driver.execute_script("""
            var callback = arguments[arguments.length - 1];
            if (window.getAllAngularTestabilities) {
                Promise.all(window.getAllAngularTestabilities().map(function(testability) {
                    return new Promise(function(resolve) {
                        testability.whenStable(resolve);
                    });
                })).then(callback);
            } else {
                callback();
            }
        """)

        driver.fullscreen_window()

        time.sleep(5)  # Additional wait for Angular to stabilize
        print("Logged in successfully")
        print("---------------" * 5)

        return driver
    else:
        login_url = elevance_login_url
        driver.get(login_url)

        wait = WebDriverWait(driver, 20)

        driver = access_shadow_root(driver)  # Access shadow root elements
        time.sleep(10)

        username_field = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
        password_field = driver.find_element(By.ID, "passWord")
        hostname_field = driver.find_element(By.ID, "hostName")
        username_field.send_keys(username)
        password_field.send_keys(password)
        hostname_field.clear()
        hostname_field.send_keys("www.mobilehealthconsumer.com")

        login_button = driver.find_element(By.XPATH, "//button[contains(.,'Login')]")
        login_button.click()

        # Wait until redirect from login page
        wait.until(lambda d: "auth/login" not in d.current_url)
        time.sleep(20)  # Extend wait if Angular takes longer

        driver.execute_script("""
            var callback = arguments[arguments.length - 1];
            if (window.getAllAngularTestabilities) {
                Promise.all(window.getAllAngularTestabilities().map(function(testability) {
                    return new Promise(function(resolve) {
                        testability.whenStable(resolve);
                    });
                })).then(callback);
            } else {
                callback();
            }
        """)
        driver.fullscreen_window()

        time.sleep(5)  # Additional wait for Angular to stabilize
        print("Logged in successfully")
        print("---------------" * 5)

        return driver


def access_shadow_root(driver):
    for el in driver.find_elements(By.CSS_SELECTOR, "app-html-component"):
        if el.is_displayed():
            try:
                # Get the shadow root content
                shadow_content = driver.execute_script("""
                    return arguments[0].shadowRoot.innerHTML;
                """, el)

                # Replace the original element with shadow content
                driver.execute_script("""
                    arguments[0].innerHTML = arguments[1];
                    arguments[0].shadowRoot.remove();
                """, el, shadow_content)
            except Exception:
                pass

    return driver


def get_html(driver):
    try:
        # Get page source with proper encoding
        html = driver.page_source.encode('utf-8', errors='ignore').decode('utf-8')
        soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')

        hidden_contents = []
        num = 0
        for el in driver.find_elements(By.CSS_SELECTOR, "app-html-component"):
            if el.is_displayed():
                shadow_content = driver.execute_script("""
                    return arguments[0].shadowRoot.innerHTML;
                """, el)
                # Handle shadow content encoding
                if shadow_content:
                    shadow_content = shadow_content.encode('utf-8', errors='ignore').decode('utf-8')
                hidden_contents.append((num, shadow_content))
            num += 1

        shadow_breakpoints = soup.find_all('app-html-component')

        for hidden_content in hidden_contents:
            hidden_soup = BeautifulSoup(hidden_content[1], "html.parser", from_encoding='utf-8')
            hidden_breakpoint = shadow_breakpoints[hidden_content[0]]
            hidden_breakpoint.append(hidden_soup)

        return soup

    except Exception as e:
        print("An error occurred in get_html:", e)
        return None


def crawl(html, elavence):
    links = []
    try:
        links = []
        for link in html.find_all('a'):
            links.append(str(link.get('href')))
    except Exception as e:
        print("An error occurred in crawl in links:", e)

    if elavence:
        # Filter links for elevance
        new_links = []
        for link in links:
            if "dashboard" in link and "angulartest" not in link:
                new_links.append("https://angulartest.mobilehealthconsumer.com" + link)
        return new_links

    return links


def get_page(driver, link=None):
    if link is None:
        time.sleep(5)
        driver.fullscreen_window()
        time.sleep(10)  # Additional wait for Angular to stabilize
        driver = access_shadow_root(driver)  # Access shadow root elements
        time.sleep(10)  # Additional wait for Angular to stabilize
    else:
        try:
            driver.get(link)
            time.sleep(15)
            driver.fullscreen_window()
            time.sleep(10)  # Additional wait for Angular to stabilize
            driver = access_shadow_root(driver) # Access shadow root elements
            time.sleep(10)  # Additional wait for Angular to stabilize
        except Exception as e:
            print(f"An error occurred while crawling {link}:", e)

    return driver
