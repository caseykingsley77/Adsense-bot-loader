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

# Number of times each link should be opened
TIMES_TO_OPEN_EACH_LINK = 2

# List of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Timeout for manual captcha solving (in seconds)
MANUAL_CAPTCHA_TIMEOUT = 120

# Time spent on each page (in minutes)
MINUTES_PER_PAGE = 3

# Number of worker threads
MAX_WORKERS = 1

# List of proxies (format: username:password:ip:port)
PROXY_LIST = [
    "moscow-zone-resi-region-us-session-eebd2648e4c6-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-9384f1a5fedf-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-f4d24f421682-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-4063be42be2b-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-ad41b4fd64bd-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-aa39fe01038e-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-9ad3083c2641-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-56a064b67fb2-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-ae742e184c9e-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
    "moscow-zone-resi-region-us-session-3cd50d50633c-sessTime-120:chidera:5a17ab2730b2fd38.iuy.us.ip2world.vip:6001",
]

# ===============================================================

import os
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from retrying import retry


def create_driver(user_agent, proxy):
    # Extract proxy details
    proxy_parts = proxy.split(":")
    if len(proxy_parts) == 4:
        username, password, ip, port = proxy_parts

    # Create a custom Firefox profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", ip)
    profile.set_preference("network.proxy.http_port", int(port))
    profile.set_preference("network.proxy.ssl", ip)
    profile.set_preference("network.proxy.ssl_port", int(port))
    profile.set_preference("general.useragent.override", user_agent)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("useAutomationExtension", False)

    # Add a script to handle proxy authentication dynamically
    profile.set_preference("javascript.enabled", True)
    auth_extension_path = os.path.join(os.getcwd(), "auth.xpi")  # Ensure auth.xpi is in the same directory
    profile.add_extension(auth_extension_path)

    service = Service('geckodriver.exe')  # Use './geckodriver' for Linux/Mac
    driver = webdriver.Firefox(service=service, firefox_profile=profile)

    # Dynamically set proxy credentials using JavaScript
    driver.get("about:blank")
    driver.execute_script(f"""
        var username = "{username}";
        var password = "{password}";
        browser.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{ authCredentials: {{ username: username, password: password }} }};
            }},
            {{ urls: ["<all_urls>"] }},
            ["blocking"]
        );
    """)

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
            "button[aria-label*='accept' i]", "button[title*='accept' i]",
            "button[aria-label*='Accept' i]", "button[title*='Accept' i]",
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


def scroll_for_ads(driver, minutes_to_scroll):
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    step_size = total_height // 10
    total_seconds = minutes_to_scroll * 60
    steps = 20
    step_duration = total_seconds / steps

    for i in range(steps):
        scroll_position = int(i / steps * total_height)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(step_duration)

    for i in range(steps):
        scroll_position = int((steps - i) / steps * total_height)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(step_duration)


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


def perform_actions(driver, global_ads_clicked):
    try:
        driver.get(BASE_URL)
        close_cookie_notice(driver)

        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        input_element.clear()
        input_element.send_keys(SEARCH_QUERY + Keys.ENTER)
        print("Search query entered and submitted.")

        search_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, SPECIFIC_SEARCH_RESULT_TEXT))
        )
        click_with_retry(driver, search_result)
        print(f"Clicked on the search result link: {SPECIFIC_SEARCH_RESULT_TEXT}.")

        scroll_for_ads(driver, MINUTES_PER_PAGE)

        for link_text in LINKS_TO_OPEN:
            for _ in range(TIMES_TO_OPEN_EACH_LINK):
                try:
                    link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                    )
                    driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                    human_like_delay()
                    print(f"Opened link: {link_text}")
                except (TimeoutException, NoSuchElementException):
                    print(f"Could not find or click link: {link_text}")

        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            scroll_for_ads(driver, MINUTES_PER_PAGE)
            if global_ads_clicked < MAX_ADS_TO_CLICK:
                ads_clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)

        print(f"Clicked on {global_ads_clicked} ads in total during this session.")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    return global_ads_clicked


def run_instance(user_agent, global_ads_clicked, proxy_list):
    try:
        # Rotate through the proxy list
        proxy = random.choice(proxy_list)
        print(f"Using proxy: {proxy}")
        driver = create_driver(user_agent, proxy)
        global_ads_clicked = perform_actions(driver, global_ads_clicked)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
        time.sleep(random.randint(5, 10))
    return global_ads_clicked


# Main script
if __name__ == "__main__":
    global_ads_clicked = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for user_agent in USER_AGENTS:
            futures.append(executor.submit(run_instance, user_agent, global_ads_clicked, PROXY_LIST))
        
        for future in as_completed(futures):
            global_ads_clicked = future.result()

    print(f"Total ads clicked across all instances: {global_ads_clicked}")