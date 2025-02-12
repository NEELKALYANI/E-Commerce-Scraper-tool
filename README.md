#  E-Commerce-Scraper-tool 

This Python script is designed to scrape product listings from **Myntra's** online shopping website. It extracts product details such as **title, description, price, image URL, and purchase link**, then saves the data into a **CSV file**. The script uses Selenium WebDriver to navigate and interact with the website dynamically.

**Features:**

* Automatically collects category links from the Myntra men's shopping page.
* Iterates through each category to extract product details.
* Scrolls through pages and navigates to the next page to gather all available products.
* Saves extracted data into a structured CSV file.
* Implements Selenium WebDriver with Chrome for automation.

**Requirements:**

Ensure you have the following installed:

* Python 3.x
* Google Chrome browser
* ChromeDriver (compatible with your Chrome version)
* Selenium library

**How It Works:**

* The script opens Myntra's men's shopping page and collects category links.
* It visits each category page, extracts product details, and stores them in a CSV file.
* The script scrolls down and navigates through pagination until all products are fetched, and then covers all products from next category.
* After completion, the browser session is closed automatically.

**Notes:**

* The script is designed specifically for Myntra's current layout. Any changes to the website may require updates to the XPath selectors.
* Ensure your ChromeDriver version matches your installed Chrome browser version.
