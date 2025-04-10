import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from retrying import retry

# =================== CONFIGURABLE PARAMETERS ===================
BASE_URL = "https://www.google.com"
TARGET_SITE = "https://nextgenentrepreneur.live/"
SEARCH_QUERY = f"site:{TARGET_SITE}"
SPECIFIC_SEARCH_RESULT_TEXT = "NextGenEntrepreneur: Home"
LINKS_TO_OPEN = [
    "How To Cancel Fitness 19 Membership in Less Then 2 Minute – 2024", 
    "How To Cancel FYE Backstage Pass without Card Online in Just 2 Minute – 2024",
    "How To Cancel Stitch Fix in Less Than 5 Minutes – 2024",
    "How To Cancel Orangetheory Membership in Just 5 Minutes 2024", 
    "How To Cancel Fitness 19 Membership in Less Then 2 Minute – 2024",
    "How To Cancel FYE Backstage Pass without Card Online in Just 2 Minute – 2024",
    "How To Cancel Stitch Fix in Less Than 5 Minutes – 2024", 
    "How To Cancel Orangetheory Membership in Just 5 Minutes 2024", 
    "How To Cancel Direct Line Car Insurance in 5 Minutes 2024", 
    "How To Cancel People Magazine Subscription in Easy Way 2024",
]
MAX_ADS_TO_CLICK = 2  # Set to 0 to skip ad clicks
TIMES_TO_OPEN_EACH_LINK = 2
MINUTES_PER_PAGE = 1
PROXY_API_URL = "https://api.360proxy.com/api/extract_ip?regions=US&num=10&protocol=http&type=json&lt=1&cate=1"
# ===============================================================

# def fetch_proxies():
#     """Fetch a fresh list of proxies from the IP2World API."""
#     try:
#         response = requests.get(PROXY_API_URL)
#         response.raise_for_status()
#         return response.text.strip().split("\r\n")
#     except requests.RequestException as e:
#         print(f"Failed to fetch proxies: {e}")
#         return []

def fetch_proxies():
    """Fetch a fresh list of proxies from the 360Proxy API."""
    try:
        response = requests.get(PROXY_API_URL)
        response.raise_for_status()
        json_data = response.json()
        if json_data.get("code") == 0:
            proxy_list = [f"{entry['ip']}:{entry['port']}" for entry in json_data["data"]]
            return proxy_list
        else:
            print(f"API returned error code: {json_data.get('code')}")
            return []
    except requests.RequestException as e:
        print(f"Failed to fetch proxies: {e}")
        return []

def get_random_user_agent():
    """Return a random user agent."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    ]
    return random.choice(user_agents)

def create_driver(proxy):
    """Create a Selenium WebDriver instance with a proxy."""
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={get_random_user_agent()}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    if proxy:
        options.add_argument(f"--proxy-server=http://{proxy}")
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    # Disable navigator.webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    return driver

def human_like_delay(min_delay=0.5, max_delay=1.5):
    """Introduce a random delay to mimic human behavior."""
    time.sleep(random.uniform(min_delay, max_delay))

def close_cookie_notice(driver):
    """Close cookie notices on the page."""
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
                        element.click()
                        human_like_delay()
                    except Exception as e:
                        print(f"Error closing cookie notice: {e}")
    except Exception as e:
        print(f"An error occurred while closing cookie notice: {e}")

def scroll_page(driver, sections=20):
    """Scroll through the page gently in sections."""
    try:
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        section_height = total_height // sections
        for i in range(sections):
            driver.execute_script(f"window.scrollTo(0, {section_height * i});")
            human_like_delay()
        driver.execute_script("window.scrollTo(0, 0);")
        human_like_delay()
    except Exception as e:
        print(f"Error scrolling page: {e}")

def click_ads(driver, global_ads_clicked):
    """Click ads up to the maximum allowed."""
    if MAX_ADS_TO_CLICK == 0:
        print("Skipping ad clicks as MAX_ADS_TO_CLICK is set to 0.")
        return 0, global_ads_clicked

    ad_selectors = [
        "div .ads-ad", "ins.adsbygoogle", "[id^='div-gpt-ad']", ".gpt-ad", ".dfp-ad",
        "[class*='sponsored-content']", "[class*='promoted-content']", "[data-ad-slot]"
    ]
    ads_clicked = 0
    for selector in ad_selectors:
        if global_ads_clicked + ads_clicked >= MAX_ADS_TO_CLICK:
            break
        ads = driver.find_elements(By.CSS_SELECTOR, selector)
        for ad in ads:
            if global_ads_clicked + ads_clicked >= MAX_ADS_TO_CLICK:
                break
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                human_like_delay()
                ad.click()
                ads_clicked += 1
                print(f"Successfully clicked ad. Total ads clicked: {global_ads_clicked + ads_clicked}")
            except Exception as e:
                print(f"Error clicking ad: {e}")
    return ads_clicked, global_ads_clicked

def click_random_link_in_ad_page(driver):
    """Click a random link on the ad page."""
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        if links:
            random_link = random.choice(links)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_link)
            human_like_delay()
            random_link.click()
            human_like_delay()
            print("Clicked a random link on the ad page.")
    except Exception as e:
        print(f"Error clicking random link in ad page: {e}")

import random

def perform_actions(driver, global_ads_clicked):
    """Perform search and interaction tasks."""
    driver.get(BASE_URL)
    try:
        # Handle Google consent forms
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        consent_selectors = [
            "button[aria-label*='Accept' i]", "button[aria-label*='Agree' i]", "button[aria-label*='Consent' i]",
            "button#L2AGLb", "button#introAgreeButton"
        ]
        for selector in consent_selectors:
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            for button in buttons:
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    human_like_delay()
                    break
    except Exception as e:
        print(f"Error handling Google consent: {e}")
    try:
        # Enter search query
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(SEARCH_QUERY + Keys.ENTER)
        human_like_delay()
        # Click on the specific search result
        result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, SPECIFIC_SEARCH_RESULT_TEXT))
        )
        result.click()
        human_like_delay()
    except Exception as e:
        print(f"Error during search or result click: {e}")
        return global_ads_clicked

    # Scroll the first page gently in 20 sections
    scroll_page(driver, sections=20)

    # Open internal links
    for link_text in LINKS_TO_OPEN:
        for _ in range(TIMES_TO_OPEN_EACH_LINK):
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                )
                driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                human_like_delay()
            except Exception as e:
                print(f"Error opening link: {link_text}")

    # Randomly select tabs for ad clicks
    tabs_with_ads = set(random.sample(driver.window_handles[1:], min(MAX_ADS_TO_CLICK, len(driver.window_handles[1:]))))

    # Interact with ads in each tab
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        scroll_page(driver, sections=20)
        close_cookie_notice(driver)

        if handle in tabs_with_ads and global_ads_clicked < MAX_ADS_TO_CLICK:
            ads_clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)
        else:
            # Skip ad clicks for this tab
            print("Skipping ad clicks for this tab.")

        time.sleep(MINUTES_PER_PAGE * 60)
        scroll_page(driver, sections=20)

        if handle in tabs_with_ads and MAX_ADS_TO_CLICK > 0:
            click_random_link_in_ad_page(driver)

    # Scroll all pages again before exiting
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        scroll_page(driver, sections=20)

    print(f"Clicked on {global_ads_clicked} ads in total during this session.")
    return global_ads_clicked

def run_instance(proxy, global_ads_clicked):
    """Run the script with a specific proxy."""
    driver = create_driver(proxy)
    try:
        global_ads_clicked = perform_actions(driver, global_ads_clicked)
    except Exception as e:
        print(f"Error with proxy {proxy}: {e}")
    finally:
        driver.quit()
        human_like_delay(5, 10)
    return global_ads_clicked

# Main script
if __name__ == "__main__":
    proxies = fetch_proxies()
    if not proxies:
        print("No proxies available. Exiting.")
        exit()

    proxy_index = 0
    total_proxies = len(proxies)
    global_ads_clicked = 0

    while global_ads_clicked < MAX_ADS_TO_CLICK:
        if proxy_index >= total_proxies:
            print("Fetching new proxies...")
            proxies = fetch_proxies()
            if not proxies:
                print("No proxies available. Exiting.")
                exit()
            proxy_index = 0
            total_proxies = len(proxies)

        proxy = proxies[proxy_index]
        print(f"Using proxy: {proxy}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_instance, proxy, global_ads_clicked)
            try:
                global_ads_clicked = future.result()
            except Exception as e:
                print(f"Error with proxy {proxy}: {e}")

        proxy_index += 1

    print("Script execution complete.")