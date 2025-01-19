from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import streamlit as st

def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver

def close_browser(driver):
    driver.quit()

@st.cache_data
def fetch_img(_driver, species_code="manher1"):
    url = f"https://ebird.org/species/{species_code}"
    _driver.get(url)
    image = _driver.find_element(By.CSS_SELECTOR, 'div.Media-content img')
    img_url = image.get_attribute('src')
    img_data = requests.get(img_url).content

    return img_data
#--------------------------------
if __name__ == "__main__":
    
    driver = initialize_browser()

    img_data = fetch_img(driver, "manher1")

    close_browser(driver)    