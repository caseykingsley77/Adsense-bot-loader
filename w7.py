import os
import zipfile
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

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
    "How To Cancel Direct Line Car Insurance in 5 Minutes 2024", 
    "How To Cancel People Magazine Subscription in Easy Way 2024",
]
MAX_ADS_TO_CLICK = 0
TIMES_TO_OPEN_EACH_LINK = 2
MINUTES_PER_PAGE = 1
# ===============================================================

# Hardcoded proxies with auth (IP:PORT:USER:PASS)
proxies = [
    "152.53.36.109:51082:OQT33R:giTECu",
    "194.163.163.10:57063:nPb1wI:aJgRQo",
    "49.12.196.34:56534:YqIlQp:XrhldJ",
    "152.53.36.109:44136:wwrN7L:lewQMy"
]

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        # Add more user agents here
    ]
    return random.choice(user_agents)

def create_proxy_extension(proxy_string):
    ip, port, user, password = proxy_string.split(":")
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """

    background_js = f"""
    chrome.proxy.settings.set({{
        value: {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{ip}",
                    port: parseInt({port})
                }},
                bypassList: ["localhost"]
            }}
        }},
        scope: "regular"
    }}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{user}",
                    password: "{password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    plugin_file = f"proxy_auth_plugin_{ip.replace('.', '_')}_{port}.zip"
    with zipfile.ZipFile(plugin_file, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file

def create_driver(proxy_string):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={get_random_user_agent()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    proxy_plugin = create_proxy_extension(proxy_string)
    options.add_extension(proxy_plugin)

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    # Prevent webdriver detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    return driver

def human_like_delay(min_delay=0.5, max_delay=1.5):
    time.sleep(random.uniform(min_delay, max_delay))

def scroll_page(driver, sections=20):
    try:
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        section_height = total_height // sections
        for i in range(sections):
            driver.execute_script(f"window.scrollTo(0, {section_height * i});")
            human_like_delay()
        driver.execute_script("window.scrollTo(0, 0);")
        human_like_delay()
    except Exception as e:
        print(f"Error scrolling: {e}")

def close_cookie_notice(driver):
    selectors = [
        "button#accept-cookies", "#onetrust-accept-btn-handler", ".accept-cookies-button",
        "[aria-label='Accept cookies']", "[data-testid='cookie-policy-dialog-accept-button']"
    ]
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                el.click()
                human_like_delay()
        except Exception:
            continue

def click_ads(driver, global_ads_clicked):
    if MAX_ADS_TO_CLICK == 0:
        return 0, global_ads_clicked

    ad_selectors = [
        "div .ads-ad", "ins.adsbygoogle", "[id^='div-gpt-ad']"
    ]
    ads_clicked = 0
    for selector in ad_selectors:
        if global_ads_clicked + ads_clicked >= MAX_ADS_TO_CLICK:
            break
        ads = driver.find_elements(By.CSS_SELECTOR, selector)
        for ad in ads:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", ad)
                human_like_delay()
                ad.click()
                ads_clicked += 1
            except Exception:
                continue
    return ads_clicked, global_ads_clicked + ads_clicked

def click_random_link_in_ad_page(driver):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        if links:
            random.choice(links).click()
            human_like_delay()
    except Exception as e:
        print(f"Error clicking link on ad page: {e}")

def perform_actions(driver, global_ads_clicked):
    driver.get(BASE_URL)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q"))).send_keys(SEARCH_QUERY + Keys.ENTER)
        human_like_delay()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, SPECIFIC_SEARCH_RESULT_TEXT))
        ).click()
    except Exception as e:
        print(f"Search failed: {e}")
        return global_ads_clicked

    scroll_page(driver)

    for link_text in LINKS_TO_OPEN:
        for _ in range(TIMES_TO_OPEN_EACH_LINK):
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                )
                driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                human_like_delay()
            except Exception:
                continue

    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        scroll_page(driver)
        close_cookie_notice(driver)

        # if global_ads_clicked < MAX_ADS_TO_CLICK:
        #     clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)
        #     if clicked > 0:
        #         click_random_link_in_ad_page(driver)

        time.sleep(MINUTES_PER_PAGE * 60)

    return global_ads_clicked

def run_instance(proxy_string, global_ads_clicked):
    driver = create_driver(proxy_string)
    try:
        global_ads_clicked = perform_actions(driver, global_ads_clicked)
    except Exception as e:
        print(f"Error using proxy {proxy_string}: {e}")
    finally:
        driver.quit()
        human_like_delay(5, 10)
        try:
            os.remove([f for f in os.listdir() if f.startswith("proxy_auth_plugin_")][0])
        except Exception:
            pass
    return global_ads_clicked

# Main logic
if __name__ == "__main__":
    proxy_index = 0
    global_ads_clicked = 0

    while global_ads_clicked < MAX_ADS_TO_CLICK:
        if proxy_index >= len(proxies):
            print("No more proxies. Exiting.")
            break

        proxy = proxies[proxy_index]
        print(f"Using proxy: {proxy}")

        with ThreadPoolExecutor(max_workers=7) as executor:
            future = executor.submit(run_instance, proxy, global_ads_clicked)
            global_ads_clicked = future.result()

        proxy_index += 1

    print("Finished session.")
