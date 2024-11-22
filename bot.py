from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import chromedriver_autoinstaller

def order_items(product_url, spending_limit, quantity_to_order=None):
    # Automatically install and set up ChromeDriver
    chromedriver_autoinstaller.install()

    # Set up Chrome options
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument('--start-maximized')  # Open browser maximized

    # Initialize the WebDriver
    service = Service()  # Chromedriver auto-installer manages the correct binary
    driver = webdriver.Chrome(service=service, options=options)

    # Open the product page
    driver.get(product_url)

    # Step 1: Add product to cart
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-button-state='ADD_TO_CART']"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(add_to_cart_button).click().perform()

    # Step 2: Go to the cart page
    cart_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/cart']"))
    )
    cart_button.click()

    # Step 3: Extract item price from cart
    item_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.price-block__primary-price"))
    )
    item_price = float(item_price_element.text.replace("$", "").replace(",", ""))
    print(f"Item price: ${item_price}")

    # Step 4: Proceed to checkout
    checkout_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Checkout']"))
    )
    checkout_button.click()

    # Step 5: Click on the 'Place Your Order' button
    button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-lg btn-block btn-primary' and @data-track='Place your Order - Contact Card']"))
    )
    button.click()

    # Close the browser
    driver.quit()

# Parameters: Specify the product URL, spending limit, and optional quantity
product_url = "https://www.bestbuy.com/site/pokemon-trading-card-game-crown-zenith-mini-tin-styles-may-vary/6527311.p?skuId=6527311"
spending_limit = 100  # Replace with the maximum amount to spend
quantity_to_order = 1  # Optional: Replace with a specific quantity if desired
order_items(product_url, spending_limit, quantity_to_order)
