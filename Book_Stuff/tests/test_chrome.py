from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

try:
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com")

    print("SUCCESS")
    print(driver.title)

    input("Press Enter to close...")

    driver.quit()

except Exception as e:
    print("FAILED")
    print(e)