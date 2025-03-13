# =================== CONFIGURABLE PARAMETERS ===================

# Base URL (Google in this case)
BASE_URL = "https://www.google.com"

# Target site to search for
TARGET_SITE = "https://lacredits.com"

# Search query to use on Google
SEARCH_QUERY = f"site:{TARGET_SITE}"

# Text of the specific search result to click
SPECIFIC_SEARCH_RESULT_TEXT = "Life2024 - Ignite Your Curiosity"

# Links to open on the target site
LINKS_TO_OPEN = [
    "Tesla or Lucid: Which Electric Car Will Dominate the Luxury Market in 2025?",
    "Forget BMW and Audi: These Luxury Cars Are the Real Kings of 2024!",
    "NordVPN’s Hidden Hack: Watch Netflix Content You Didn’t Know Existed!",
    "How to Invest in Real Estate for Passive Income in 2025",
    "USA: «Save Money on Home Insurance with These Proven Strategies! »",
    "Canada: «Canadians Are Saving Thousands on Health Insurance with This One Trick! »",
    "Grammarly vs. Human Editors: Who Wins the Battle for Flawless Writing?",
    "Mazda USA: The Future of Electric Vehicles and Why It’s Worth Your Attention",
    "The Secret to Finding the Best Business Software: A Deep Dive into Capterra",
    "Unlock Your Creative Potential: How Adobe Tools Can Transform Your Workflow",
]

# Maximum number of ads to click
MAX_ADS_TO_CLICK = 5

# List of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F; rv:89.0) Gecko/89.0 Firefox/89.0",
]

# Number of worker threads
MAX_WORKERS = 1

# ===============================================================

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from retrying import retry

def create_driver(user_agent):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("general.useragent.override", user_agent)
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference("useAutomationExtension", False)
    service = Service('geckodriver.exe')  # Use './geckodriver' for Linux/Mac
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def click_with_retry(driver, element):
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)

def human_like_delay():
    time.sleep(random.uniform(0.5, 1.5))

def close_cookie_notice(driver):
    try:
        selectors = [
            "div.cookie-notice-container", "button.accept-cookies", "div.cookie-consent",
            "button#accept-cookies", "#onetrust-accept-btn-handler", ".accept-cookies-button",
            "[aria-label='Accept cookies']", "[data-testid='cookie-policy-dialog-accept-button']",
            "button[aria-label*='accept' i]", "button[title*='accept' i]", "button[aria-label*='Accept' i]", "button[title*='Accept' i]",
            "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll", ".css-47sehv", "#rcc-confirm-button",
            ".cl-accept-all", ".js-accept-all-cookies", "#js-cookie-accept", ".js-accept-cookies",
            "[data-testid='accept-all-cookies']", "[data-testid='cookie-banner-accept-all']"
        ]
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                for element in elements:
                    try:
                        click_with_retry(driver, element)
                        human_like_delay()
                    except Exception as e:
                        print(f"Error closing cookie notice: {e}")
    except Exception as e:
        print(f"An error occurred while closing cookie notice: {e}")

def scroll_for_ads(driver):
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, random.randint(100, 300)):
        driver.execute_script(f"window.scrollTo(0, {i});")
        human_like_delay()
    driver.execute_script("window.scrollTo(0, 0);")
    human_like_delay()

def click_ads(driver, global_ads_clicked):
    ad_selectors = [
        "div .ads-ad", "ins.adsbygoogle", "[id^='div-gpt-ad']", ".gpt-ad", ".dfp-ad",
        "[class*='sponsored-content']", "[class*='promoted-content']", "[data-ad-slot]"
    ]

    ads_clicked = 0
    for selector in ad_selectors:
        ads = driver.find_elements(By.CSS_SELECTOR, selector)
        for ad in ads:
            if global_ads_clicked >= MAX_ADS_TO_CLICK:
                return ads_clicked, global_ads_clicked
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                human_like_delay()
                click_with_retry(driver, ad)
                ads_clicked += 1
                global_ads_clicked += 1
                print(f"Successfully clicked ad. Total ads clicked: {global_ads_clicked}")
            except Exception as e:
                print(f"Error clicking ad: {e}")
                continue
    return ads_clicked, global_ads_clicked

def open_link_in_page(driver):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        if links:
            link = random.choice(links)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
            human_like_delay()
            click_with_retry(driver, link)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            human_like_delay()
    except Exception as e:
        print(f"Error opening link in page: {e}")

def handle_google_consent(driver):
    try:
        consent_selectors = [
            "button[aria-label*='Accept' i]",
            "button[aria-label*='Agree' i]",
            "button[aria-label*='Consent' i]",
            "button[aria-label*='Accepter' i]", 
            "button[aria-label*='Akzeptieren' i]",
            "button[aria-label*='Accetta' i]",
            "button#L2AGLb",  # New selector for Google consent
            "button#introAgreeButton"  # Another new selector for Google consent
        ]
        
        for selector in consent_selectors:
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            for button in buttons:
                if button.is_displayed() and button.is_enabled():
                    try:
                        driver.execute_script("arguments[0].click();", button)
                        human_like_delay()
                        return
                    except:
                        continue
    except Exception as e:
        print(f"Error handling Google consent: {e}")

def perform_actions(driver, global_ads_clicked):
    try:
        driver.get(BASE_URL)
        handle_google_consent(driver)

        # Enter search query
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        input_element.clear()
        input_element.send_keys(SEARCH_QUERY + Keys.ENTER)
        print("Search query entered and submitted.")

        # Click on the specific search result
        try:
            search_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, SPECIFIC_SEARCH_RESULT_TEXT))
            )
            click_with_retry(driver, search_result)
            print(f"Clicked on the search result link: {SPECIFIC_SEARCH_RESULT_TEXT}.")
        except (TimeoutException, NoSuchElementException):
            print(f"Could not find or click the search result: {SPECIFIC_SEARCH_RESULT_TEXT}.")
            return global_ads_clicked

        # Scroll the page
        scroll_for_ads(driver)

        # Open internal links
        for link_text in LINKS_TO_OPEN:
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                )
                driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                human_like_delay()
                print(f"Opened link: {link_text}")
            except (TimeoutException, NoSuchElementException):
                print(f"Could not find or click link: {link_text}")

        # Switch to each opened tab and interact with ads
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            scroll_for_ads(driver)
            if global_ads_clicked < MAX_ADS_TO_CLICK:
                ads_clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)
            open_link_in_page(driver)

        print(f"Clicked on {global_ads_clicked} ads in total during this session.")

    except Exception as e:
        print(f"An error occurred during execution: {e}")
    
    return global_ads_clicked

def run_instance(user_agent, global_ads_clicked):
    driver = create_driver(user_agent)
    try:
        global_ads_clicked = perform_actions(driver, global_ads_clicked)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        time.sleep(random.randint(5, 10))
    
    return global_ads_clicked

# Main script
if __name__ == "__main__":
    global_ads_clicked = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for user_agent in USER_AGENTS:
            futures.append(executor.submit(run_instance, user_agent, global_ads_clicked))
        
        for future in as_completed(futures):
            global_ads_clicked = future.result()

    print(f"Total ads clicked across all instances: {global_ads_clicked}")