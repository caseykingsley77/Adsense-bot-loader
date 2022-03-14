# README for Automated Script (Robot.py)

This guide will help you set up and run the `Robot.py` script. The script automates web browsing actions, including clicking ads and navigating through pages. Below are detailed instructions to help you get started.

---

## **Contents**
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Running the Script](#running-the-script)
5. [Customizing the Script](#customizing-the-script)
   - [Changing the Target Website](#changing-the-target-website)
   - [Modifying Pages to Visit](#modifying-pages-to-visit)
   - [Adjusting Proxies](#adjusting-proxies)
   - [Tweaking User Agents](#tweaking-user-agents)
   - [Configuring Maximum Workers](#configuring-maximum-workers)
6. [Managing Proxies](#managing-proxies)
7. [Troubleshooting](#troubleshooting)
8. [Important Notes](#important-notes)

---

## **Introduction**

The `Robot.py` script is designed to automate interactions with a website. It uses Selenium to simulate human-like behavior, such as clicking ads, navigating links, and handling cookies. This script is useful for tasks like testing websites or automating repetitive actions.

---

## **Prerequisites**

Before running the script, ensure you have the following:

- **Python Installed**: Make sure Python 3.x is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).
- **vscode Installed**: Make sure VSCODE is installed on your computer. You can download it from [visualstudio.com](https://code.visualstudio.com/download).
- **Chrome Browser**: Ensure that Google Chrome is installed on your system.
- **Chromedriver**: The script includes a `chromedriver` file. Ensure its version matches your installed Chrome browser version.

---

## **Setup Instructions**

### Step 1: Install Dependencies
1. Open a terminal or command prompt in the folder containing the script.
2. Run the following command to install all required libraries:
   ```bash
   python -m venv venv
   ```
   1. On Windows:
   ```bash
   venv\Scripts\activate
   ```
    2. On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   ```bash
   pip install -r requirements.txt
   ```
   This installs all dependencies listed in the `requirements.txt` file.

### Step 2: Activate Virtual Environment (Not Optional)
If you want to use the provided virtual environment (`venv`):
1. On Windows:
   ```bash
   venv\Scripts\activate
   ```
2. On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

---

## **Running the Script**

### Step 1: Open Terminal/Command Prompt
Navigate to the folder where the `Robot.py` file is located.

### Step 2: Execute the Script
Run the following command:
```bash
python Robot.py
```
The script will start executing, opening multiple browser windows and performing automated actions.

---

## **Customizing the Script**

### Changing the Target Website
To change the website the script interacts with:
1. Open the `Robot.py` file in a text editor.
2. Locate the line where the search query is defined:
   ```python
   input_element.send_keys("site:https://lacredits.com" + Keys.ENTER)
   ```
3. Replace `https://lacredits.com` with the URL of your desired website.
4. Save the file.

### Modifying Pages to Visit
To modify the pages the script visits:
1. Open the `Robot.py` file in a text editor.
2. Locate the `links_to_open` list:
   ```python
   links_to_open = [
       "Tesla or Lucid: Which Electric Car Will Dominate the Luxury Market in 2025?",
       "Forget BMW and Audi: These Luxury Cars Are the Real Kings of 2024!",
       ...
   ]
   ```
3. Replace the page titles with the titles of the pages you want to visit.
4. Save the file.

### Adjusting Proxies
To adjust the proxies used by the script:
1. Open the `Robot.py` file in a text editor.
2. Locate the `proxies` list:
   ```python
   proxies = [
       "159.203.91.171:50474",
       "159.203.91.171:50474",
       ...
   ]
   ```
3. Add or replace the proxy entries with your new proxies.
4. Save the file.

### Tweaking User Agents
To tweak the user agents used by the script:
1. Open the `Robot.py` file in a text editor.
2. Locate the `user_agents` list:
   ```python
   user_agents = [
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
       ...
   ]
   ```
3. Add or replace the user agent strings with your desired ones.
4. Save the file.

### Configuring Maximum Workers
To configure the number of threads (workers) the script runs simultaneously:
1. Open the `Robot.py` file in a text editor.
2. Locate the `ThreadPoolExecutor` line:
   ```python
   with ThreadPoolExecutor(max_workers=1) as executor:
   ```
3. Change the `max_workers` value to the desired number of threads. For example, to allow 5 threads:
   ```python
   with ThreadPoolExecutor(max_workers=5) as executor:
   ```
4. Save the file.

---

## **Managing Proxies**

Proxies are used to route the script's traffic through different IP addresses. If your current proxies expire, follow these steps to update them:

### Step 1: Obtain New Proxies
Get a list of new proxies from a reliable provider.

### Step 2: Update the Proxies List
1. Open the `Robot.py` file in a text editor.
2. Locate the `proxies` list:
   ```python
   proxies = [
       "159.203.91.171:50474",
       "159.203.91.171:50474",
       ...
   ]
   ```
3. Replace the existing proxy entries with your new proxies.
4. Save the file.

---

## **Troubleshooting**

### Common Issues and Solutions

1. **Error: Chromedriver Version Mismatch**
   - Ensure the `chromedriver` version matches your installed Chrome browser version. Download the correct version from [chromedriver.chromium.org](https://chromedriver.chromium.org/).

2. **Error: Missing Dependencies**
   - Reinstall dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **Script Stops Unexpectedly**
   - Check the terminal for error messages. Common issues include invalid proxies or changes in the target website structure.

4. **Cookies Not Closing**
   - Ensure the selectors in the `close_cookie_notice` function match the cookie notice elements on the target website.

---

## **Important Notes**

- **Legal Considerations**: Ensure you have permission to automate interactions with the target website. Unauthorized use may violate terms of service.
- **Performance**: Running the script with too many threads (e.g., `max_workers`) can slow down your system. Start with a lower number and adjust as needed.
- **Proxy Rotation**: Regularly update proxies to avoid being blocked by websites.
- **Backup**: Before making changes to the script, create a backup of the original file.

---

By following this guide, you should be able to successfully set up and run the `Robot.py` script. If you encounter any issues, feel free to reach out for assistance. Happy scripting!