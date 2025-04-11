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

# List of proxies
proxies = [
    "37.221.193.221:12719",
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

def create_driver(proxy, user_agent):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def close_cookie_notice(driver):
    try:
        selectors = ["div.cookie-notice-container", "button.accept-cookies", "div.cookie-consent", "button#accept-cookies"]
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                for element in elements:
                    try:
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element)).click()
                        time.sleep(1)
                    except ElementClickInterceptedException:
                        print(f"Element click intercepted while trying to close cookie notice: {selector}")
    except Exception as e:
        print(f"An error occurred while closing cookie notice: {e}")

def scroll_for_ads(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

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
        for ad in ads[:5]:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ad))
                driver.execute_script("arguments[0].scrollIntoView();", ad)
                time.sleep(1)
                ad.click()
                ads_clicked += 1
                global_ads_clicked += 1
                WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(driver.window_handles) + 1))
                driver.switch_to.window(driver.window_handles[-1])

                try:
                    logo_link = driver.find_element(By.CSS_SELECTOR, "a[aria-label*='logo'], a[title*='logo'], img[alt*='logo']")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(logo_link))
                    logo_link.click()
                except NoSuchElementException:
                    try:
                        other_link = driver.find_element(By.CSS_SELECTOR, "a, button")
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(other_link))
                        other_link.click()
                    except NoSuchElementException:
                        print("No clickable links or buttons found on the ad page.")
                
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
                if ads_clicked >= 5:
                    return ads_clicked, global_ads_clicked
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, WebDriverException) as e:
                print(f"Error clicking ad: {e}")
    
    return ads_clicked, global_ads_clicked

def open_link_in_page(driver):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        if links:
            link = random.choice(links)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))
            link.click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error opening link in page: {e}")

def handle_google_consent(driver):
    try:
        consent_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CXQnmb"))
        )
        
        customize_button = driver.find_element(By.XPATH, "//button[@aria-label='Customize']")
        customize_button.click()
        
        time.sleep(2)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        confirm_button = driver.find_element(By.XPATH, "//button[@aria-label='Confirm']")
        confirm_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "CXQnmb"))
        )
    except TimeoutException:
        print("Consent form not found or already handled.")
    except Exception as e:
        print(f"Error handling Google consent: {e}")

def perform_actions(driver, global_ads_clicked):
    try:
        driver.get("https://google.com")
        
        handle_google_consent(driver)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        input_element = driver.find_element(By.NAME, "q")
        input_element.clear()
        input_element.send_keys("site:https://myblogsoft.com/" + Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Myblogsoft.com - Tu Sitio Web del Gaming")))
        search_results = driver.find_elements(By.PARTIAL_LINK_TEXT, "Myblogsoft.com - Tu Sitio Web del Gaming")
        if search_results:
            search_results[0].click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        links_to_open = [
    "Generador de Nombre Tryhard para Fortnite",
    "Generador de Nombres para Free Fire",
    "¿Qué ensamblador de tarjetas gráficas es el más fiable?",
    "¿Cuál es la mejor tarjeta de vídeo para PC?",
    "¿Qué diferencia hay entre una RAM gamer y una normal?",
    "¿Qué es mejor una pantalla LCD o LED?",
    "Monitor Gaming ¿Cómo saber si es bueno?",
    "PC Gamer: ¿Cómo saber si mi PC es buena para juegos?",
    "¿Cuál es el mejor procesador AMD vs Intel?",
    "¿Qué procesador Gaming es bueno para juegos?",
   
]
        for link_text in links_to_open:
            for _ in range(3):
                try:
                    link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
                    )
                    driver.execute_script("window.open(arguments[0].href, '_blank');", link)
                except (TimeoutException, NoSuchElementException):
                    print(f"Could not find or click link: {link_text}")

        total_ads_clicked = 0
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            
            scroll_for_ads(driver)
            close_cookie_notice(driver)
            if total_ads_clicked < 5:
                ads_clicked, global_ads_clicked = click_ads(driver, global_ads_clicked)
                total_ads_clicked += ads_clicked
        
        print(f"Clicked on {total_ads_clicked} ads in total during this session.")

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
global_ads_clicked = 0
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = []
    for proxy in proxies:
        for user_agent in user_agents:
            futures.append(executor.submit(run_instance, proxy, user_agent, global_ads_clicked))
    
    for future in as_completed(futures):
        global_ads_clicked = future.result()

print(f"Total ads clicked across all proxies: {global_ads_clicked}")