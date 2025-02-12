from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service('myntra_shopping/chromedriver.exe'), options=options)
wait = WebDriverWait(driver, 10)

csv_filename = "myntra_shopping/myntra_products.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Price", "Image", "Shop Here"])

def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def collect_category_links():
    url = "https://www.myntra.com/shop/men"
    driver.get(url)
    
    xpaths = [
        '/html/body/div[2]/div/main/div/div[6]/div/div/div',
        '/html/body/div[2]/div/main/div/div[7]/div/div/div',
        '/html/body/div[2]/div/main/div/div[8]/div/div/div'
    ]

    category_links = []
    for xpath in xpaths:
        try:
            row = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            row_links = row.find_elements(By.TAG_NAME, 'a')
            category_links.extend([link.get_attribute('href') for link in row_links if link.get_attribute('href')])
        except Exception as e:
            print(f"Error collecting category links: {e}")

    return category_links

def click_next_page():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/main/div[3]/div[2]/div/div[2]/section/div[2]/ul/li[4]")))
        next_button.click()
        time.sleep(3)
        return True
    
    except Exception as e:
        print(f"Next button not found or not clickable: {e}")
        return False

def fetch_category_products(category_link):
    driver.get(category_link)
    time.sleep(5)
    scroll_page()

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        while True:
            try:
                product_section = wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'results-base')]")))
                prod_list = product_section.find_elements(By.TAG_NAME, 'li')

                category_name = driver.find_element(By.XPATH, "/html/body/div[2]/div/main/div[1]/div/ul/li[3]/span").text
                writer.writerow([category_name])  

                for prod in prod_list:
                    try:
                        title = prod.find_element(By.XPATH, ".//h3").text.strip() if prod.find_elements(By.XPATH, ".//h3") else "No Title"
                        description = prod.find_element(By.XPATH, ".//h4").text.strip() if prod.find_elements(By.XPATH, ".//h4") else "No Description"
                        price = prod.find_element(By.XPATH, ".//span[contains(@class, 'product-discountedPrice')]").text.strip() if prod.find_elements(By.XPATH, ".//span[contains(@class, 'product-discountedPrice')]") else "No Price"
                        image_element = prod.find_element(By.XPATH, "/html/body/div[2]/div/main/div[3]/div[2]/div/div[2]/section/ul/li[1]/a/div[1]/div/div/div/picture/img").get_attribute("src") if prod.find_elements(By.XPATH, "/html/body/div[2]/div/main/div[3]/div[2]/div/div[2]/section/ul/li[1]/a/div[1]/div/div/div/picture/img") else "No Image"
                        buy_link_elements = prod.find_elements(By.XPATH, ".//a[contains(@href, '/buy')]")
                        buy_link = buy_link_elements[0].get_attribute("href") if buy_link_elements else "No Link"
                        
                        if buy_link != "No Link" and image_element != "No Image":
                            writer.writerow([title, description, price, image_element, buy_link])
                    except Exception as e:
                        print(f"Skipping a product due to error: {e}")
                        continue  

            except Exception as e:
                print(f"Error fetching product details: {e}")

            if not click_next_page():
                break  # Stop if no next page is available

def main():
    category_links = collect_category_links()
    for category_link in category_links:
        fetch_category_products(category_link)

    driver.quit()

if __name__ == "__main__":
    main()
