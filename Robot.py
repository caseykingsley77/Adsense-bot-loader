from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, WebDriverException
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from retrying import retry

# List of proxies
# Where to input proxies
proxies = [
    "43.130.58.109:8433",
    "43.130.58.109:8441",
    "43.153.73.54:8159",
    "43.135.159.230:9495",
    "43.153.73.54:8211",
    "43.153.73.54:8143",
    "43.130.62.247:9352",
    "43.153.73.54:8214",
    "43.159.28.58:8735",
    "43.159.28.58:8759",
    "43.159.28.58:8696",
    "43.130.58.109:8458",
    "43.153.73.54:8142",
    "43.135.159.230:9491",
    "43.159.28.58:8736",
    "43.153.73.54:8216",
    "43.135.159.230:9483",
    "43.130.58.109:8435",
    "43.130.58.109:8478",
    "43.135.159.230:9499",
    "43.153.73.54:8125",
    "43.135.159.230:9542",
    "43.130.62.247:9380",
    "43.153.73.54:8136",
    "43.135.159.230:9492",
    "43.159.28.58:8705",
    "43.153.73.54:8122",
    "43.153.73.54:8170",
    "43.130.62.247:9387",
    "43.135.159.230:9516",
    "43.159.28.58:8776",
    "43.135.159.230:9459",
    "43.153.73.54:8150",
    "43.135.159.230:9480",
    "43.130.58.109:8426",
    "43.159.28.58:8711",
    "43.135.159.230:9463",
    "43.135.159.230:9537",
    "43.153.73.54:8192",
    "43.135.159.230:9457",
    "43.159.28.58:8757",
    "43.135.159.230:9518",
    "43.153.73.54:8155",
    "43.135.159.230:9551",
    "43.135.159.230:9501",
    "43.135.159.230:9546",
    "43.130.58.109:8428",
    "43.159.28.58:8714",
    "43.130.62.247:9337",
    "43.159.28.58:8710",
    "43.153.73.54:8167",
    "43.135.159.230:9475",
    "43.153.73.54:8210",
    "43.130.62.247:9418",
    "43.135.159.230:9536",
    "43.153.73.54:8127",
    "43.135.159.230:9543",
    "43.130.58.109:8510",
    "43.135.159.230:9502",
    "43.130.62.247:9405",
    "43.153.73.54:8182",
    "43.130.62.247:9406",
    "43.159.28.58:8722",
    "43.135.159.230:9524",
    "43.135.159.230:9454",
    "43.135.159.230:9470",
    "43.130.62.247:9411",
    "43.130.58.109:8436",
    "43.135.159.230:9494",
    "43.159.28.58:8727",
    "43.130.62.247:9399",
    "43.135.159.230:9474",
    "43.135.159.230:9534",
    "43.135.159.230:9460",
    "43.130.58.109:8512",
    "43.130.62.247:9363",
    "43.153.73.54:8164",
    "43.130.62.247:9374",
    "43.159.28.58:8728",
    "43.135.159.230:9544",
    "43.130.58.109:8437",
    "43.135.159.230:9547",
    "43.130.58.109:8431",
    "43.153.73.54:8184",
    "43.159.28.58:8734",
    "43.130.58.109:8432",
    "43.130.58.109:8488",
    "43.159.28.58:8706",
    "43.130.58.109:8496",
    "43.135.159.230:9476",
    "43.153.73.54:8205",
    "43.153.73.54:8141",
    "43.135.159.230:9538",
    "43.153.73.54:8131",
    "43.159.28.58:8761",
    "43.130.62.247:9342",
    "43.153.73.54:8213",
    "43.159.28.58:8726",
    "43.130.62.247:9371",
    "43.130.62.247:9349",
    "43.130.58.109:8430",
    "43.130.62.247:9365",
    "43.135.159.230:9469",
    "43.130.58.109:8499",
    "43.159.28.58:8766",
    "43.159.28.58:8779",
    "43.130.58.109:8493",
    "43.135.159.230:9489",
    "43.130.62.247:9385",
    "43.130.62.247:9341",
    "43.130.62.247:9333",
    "43.130.58.109:8449",
    "43.130.58.109:8484",
    "43.130.62.247:9402",
    "43.153.73.54:8123",
    "43.135.159.230:9465",
    "43.159.28.58:8772",
    "43.159.28.58:8762",
    "43.159.28.58:8695",
    "43.130.58.109:8434",
    "43.135.159.230:9527",
    "43.135.159.230:9496",
    "43.135.159.230:9553",
    "43.135.159.230:9462",
    "43.159.28.58:8749",
    "43.159.28.58:8739",
    "43.135.159.230:9513",
    "43.135.159.230:9548",
    "43.153.73.54:8130",
    "43.130.62.247:9396",
    "43.130.58.109:8518",
    "43.135.159.230:9504",
    "43.159.28.58:8704",
    "43.153.73.54:8166",
    "43.159.28.58:8767",
    "43.153.73.54:8153",
    "43.153.73.54:8202",
    "43.153.73.54:8206",
    "43.130.58.109:8445",
    "43.153.73.54:8193",
    "43.130.58.109:8456",
    "43.130.62.247:9382",
    "43.153.73.54:8178",
    "43.135.159.230:9515",
    "43.130.58.109:8521"
]




# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F; rv:89.0) Gecko/89.0 Firefox/89.0"
]

current_proxy_index = -1

def get_next_proxy():
    global current_proxy_index
    current_proxy_index = (current_proxy_index + 1) % len(proxies)
    return proxies[current_proxy_index]

def create_driver(proxy, user_agent):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # service = Service('./chromedriver') #Remove '#' at the begining of the line to use it in linux
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
        "div.ads-ad", "div.commercial-unit-desktop-top", "div.commercial-unit-desktop-rhs",
        "div[data-text-ad='1']", "div.cfxYMc.JfZTW.c4Djg", "iframe[name^='google_ads_iframe']",
        "ins.adsbygoogle", "div[id^='google_ads_iframe']", "a[data-vars-cta-type='ad']",
        ".adsbygoogle", "[id^='div-gpt-ad']", ".gpt-ad", ".dfp-ad", ".ad-container",
        "[class*='sponsored-content']", "[class*='promoted-content']", "[data-ad-slot]"
    ]

    ads_clicked = 0
    for selector in ad_selectors:
        ads = driver.find_elements(By.CSS_SELECTOR, selector)
        for ad in ads:
            if global_ads_clicked >= 5:
                return ads_clicked, global_ads_clicked
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                human_like_delay()

                initial_window_count = len(driver.window_handles)
                click_with_retry(driver, ad)
                
                try:
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(initial_window_count + 1))
                    ads_clicked += 1
                    global_ads_clicked += 5
                    print(f"Successfully clicked ad. Total ads clicked: {global_ads_clicked}")
                except TimeoutException:
                    print("Ad click didn't open a new window, moving to next ad.")
                    continue

                driver.switch_to.window(driver.window_handles[-1])

                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                close_cookie_notice(driver)

                # Try to click on home page or logo
                home_selectors = ["a.logo", "a.home", "a[href='/']", "a[href='./']", "a[href='index.html']"]
                home_clicked = False
                for home_selector in home_selectors:
                    try:
                        home_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, home_selector)))
                        click_with_retry(driver, home_link)
                        home_clicked = True
                        break
                    except:
                        continue

                if not home_clicked:
                    # If home/logo not found, click on a random link
                    links = driver.find_elements(By.TAG_NAME, "a")
                    if links:
                        random_link = random.choice(links)
                        click_with_retry(driver, random_link)

                scroll_amount = random.randint(100, 500)
                driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
                human_like_delay()

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
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

# def handle_google_consent(driver):
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        
#         consent_selectors = [
#             "button[aria-label*='Accept' i]",
#             "button[aria-label*='Agree' i]",
#             "button[aria-label*='Consent' i]",
#             "button[aria-label*='Accepter' i]",
#             "button[aria-label*='Akzeptieren' i]",
#             "button[aria-label*='Accetta' i]",
#             "button:not([aria-label]):not([type='submit'])",
#             "div[role='button']",
#             "input[type='submit']",
#             "a[role='button']"
#         ]
        
#         for selector in consent_selectors:
#             buttons = driver.find_elements(By.CSS_SELECTOR, selector)
#             for button in buttons:
#                 if button.is_displayed() and button.is_enabled():
#                     try:
#                         driver.execute_script("arguments[0].click();", button)
#                         human_like_delay()
#                         return
#                     except:
#                         continue

#         # If no button found, try to find any clickable element within the form
#         form = driver.find_element(By.TAG_NAME, "form")
#         clickable_elements = form.find_elements(By.CSS_SELECTOR, "button, input[type='submit'], a[role='button']")
#         if clickable_elements:
#             click_with_retry(driver, random.choice(clickable_elements))
        
        WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.TAG_NAME, "form")))
    except Exception as e:
        print(f"Error handling Google consent: {e}")

def perform_actions(driver, global_ads_clicked):
    try:
        driver.get("https://google.com")
        
        handle_google_consent(driver)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        input_element = driver.find_element(By.NAME, "q")
        input_element.clear()
        input_element.send_keys("site:https://nationaleconomy.com" + Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "National Economy Newspaper - Business News, Nigerian ...")))
        search_results = driver.find_elements(By.PARTIAL_LINK_TEXT, "National Economy Newspaper - Business News, Nigerian ...")
        if search_results:
            search_results[0].click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        links_to_open = [
     "NGX Group, CSCS Commit To Gender Equality", 
     "Nigeria’s In-country Refining And Import Substitution Imbroglio",
     "Shell’s $5bn Bonga Field: Iseyi Gas Project To Reshape Energy Sector",
     "Building Strong Workplace Relationships", 
     "Need To Accelerate Investment In Digital Transformation",
     "Heirs Energies To Drive Nigeria’s Oil Production Growth",
     "Safety App To Tackle Insecurity Issues, Delayed Response Debuts", 
     "Lagos-Calabar Highway: A Game-changer Or Costly Gamble", 
     "Transcorp Group Seeks Diversity In Driving Africa’s Energy Transformation", 
     "CSO Backs Tesla Amid Cybertruck Explosion Allegation",
]
        
        
        for link_text in links_to_open:
            for _ in range(3):
                try:
                    link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                    )
                    driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                    human_like_delay()
                except (TimeoutException, NoSuchElementException):
                    print(f"Could not find or click link: {link_text}")

        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            
            human_like_delay()
            scroll_for_ads(driver)
            human_like_delay()
            close_cookie_notice(driver)
            if global_ads_clicked < 5:
                ads_clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)
            human_like_delay()
            
            if global_ads_clicked >= 5:
                break
        
        print(f"Clicked on {global_ads_clicked} ads in total during this session.")

        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            close_cookie_notice(driver)
            open_link_in_page(driver)

    except Exception as e:
        print(f"An error occurred during execution: {e}")
    
    return global_ads_clicked

def run_instance(proxy, user_agent, global_ads_clicked):
    driver = create_driver(proxy, user_agent)
    try:
        global_ads_clicked = perform_actions(driver, global_ads_clicked)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        time.sleep(random.randint(5, 10))
    
    return global_ads_clicked

# Main script

global_ads_clicked = 5
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = []
    for proxy in proxies:
        for user_agent in user_agents:
            futures.append(executor.submit(run_instance, proxy, user_agent, global_ads_clicked))
    
    for future in as_completed(futures):
        global_ads_clicked = future.result()

print(f"Total ads clicked across all proxies: {global_ads_clicked}")