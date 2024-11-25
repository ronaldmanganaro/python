from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import chromedriver_autoinstaller

import argparse
import subprocess
import time
import random

spending_limit = 100  # Replace with the maximum amount to spend
quantity_to_order = 1  # Optional: Replace with a specific quantity if desired
        
def parse_arguents():
    parser = argparse.ArgumentParser(description="bot that buys shit")
    parser.add_argument('-l', '--link', help='link to the item you want to buy')
    parser.add_argument('-t', '--test', help='test flow wihtout purchase step', action='store_true', default=False)
    parser.add_argument('-p', '--preorder', help='set if preording product', action='store_true', default=False)
    parser.add_argument('-s', '--store', help='set if store product', default="bestbuy")
    
    return parser.parse_args()

def start_headless():
    #subprocess.run(['start', 'chrome', '--remote-debugging-port=9222', '--user-data-dir="C:\Users\MrCool\AppData\Local\Google\Chrome\User Data"', '--profile-directory="default"'])
    bestbuy_paypal(args.link, spending_limit, quantity_to_order)

def bestbuy_paypal(product_url, spending_limit, quantity_to_order=None):
    # Automatically install and set up ChromeDriver
    chromedriver_autoinstaller.install()

    # Set up Chrome options
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument('--start-maximized')  # Open browser maximized
    #options.add_argument('--disable-gpu')
    #options.add_argument('--headless')
    options.add_argument('--user-data-dir=\"C:\\Users\\MrCool\\AppData\\Local\\Google\\Chrome\\User Data\"')
    options.add_argument('--profile-directory="default"')
    
    # Initialize the WebDriver
    service = Service()  # Chromedriver auto-installer manages the correct binary
    driver = webdriver.Chrome(service=service, options=options)

    # Open the product page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    
    driver.get(product_url)
    driver.save_screenshot("openproduct.png")

    # Define parameters
    timeout = 608400  # Total wait time in seconds
    min_refresh_interval = 20  # Minimum refresh interval in seconds
    max_refresh_interval = 50  # Maximum refresh interval in seconds

    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Wait for up to 5 seconds to find the element
            if args.preorder:
                add_to_cart_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-button-state='PRE_ORDER']"))
                )
            else:
                add_to_cart_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-button-state='ADD_TO_CART']"))
                )
                        
            shipping_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Shipping')]"))
            )
            
            if add_to_cart_button:
                print("Button is clickable!")
                shipping_button.click()
                actions = ActionChains(driver)
                actions.move_to_element(add_to_cart_button).click().perform()
                break  # Exit the loop when the condition is satisfied
        except Exception as e:
            # If the element is not found or not clickable, handle the exception
            print("Waiting for the button...")

        # Generate a random refresh interval
        refresh_interval = random.randint(min_refresh_interval, max_refresh_interval)
        print(f"Refreshing the page in {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        driver.refresh()

    # Cleanup
    if time.time() - start_time >= timeout:
        print("Timed out waiting for the button.")


    # Step 2: Go to the cart page
    cart_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/cart']"))
    )
    cart_button.click()

    # Step 3: Extract item price from cart
    #item_price_element = WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, "div.price-block__primary-price"))
    #)
    #item_price = float(item_price_element.text.replace("$", "").replace(",", ""))
    #print(f"Item price: ${item_price}")
    
     # Step 5: Click on the 'Place Your Order' button
    paypal_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-track='Cart_PayPal_Checkout_Button']"))
    )
    paypal_button.click()
    
    # Step 5: Click on the 'Place Your Order' button
    paypal_review_order_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='payment-submit-btn']"))
    )
    paypal_review_order_button.click() 
        
    # Step 5: Click on the 'Place Your Order' button
    order_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-lg btn-block btn-primary' and @data-track='Place your Order - Contact Card']"))
    )
    #print("PLACED ORDER")
    
    if args.test == True:
        print("Test ORDERED")
    else:
        print("REALLY ORDERED")
        order_button.click()
    
    # Close the browser
    driver.quit()


def target(product_url, spending_limit, quantity_to_order=None):
    # Automatically install and set up ChromeDriver
    chromedriver_autoinstaller.install()

    # Set up Chrome options
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument('--start-maximized')  # Open browser maximized
    #options.add_argument('--disable-gpu')
    #options.add_argument('--headless')
    options.add_argument('--user-data-dir=\"C:\\Users\\MrCool\\AppData\\Local\\Google\\Chrome\\User Data\"')
    options.add_argument('--profile-directory="default"')
    
    # Initialize the WebDriver
    service = Service()  # Chromedriver auto-installer manages the correct binary
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    print(f"open {product_url}")
    driver.get(product_url)
    
    # Define parameters
    timeout = 608400  # Total wait time in seconds
    min_refresh_interval = 13  # Minimum refresh interval in seconds
    max_refresh_interval = 23  # Maximum refresh interval in seconds

    start_time = time.time()
    buy_now_button = None
    
    while True:
        try:
            # Attempt to find the Buy Now button
            buy_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-test='buy-now-button']"))
            )
            
            if buy_now_button:
                print("Buy Now button is clickable!")

                # Find the dropdown and click it
                dropdown_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='select-:rg:']"))
                )
                dropdown_button.click()

                # Wait for the <ul> element to be present and updated
                ul_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//ul[@class='sc-5a11d645-0 gPhogk']"))
                )
                
                # Extract all <li> elements inside the <ul>
                list_items = ul_element.find_elements(By.TAG_NAME, 'li')
                
                # Extract the numbers, convert them to integers, and find the largest
                numbers = [int(item.text) for item in list_items if item.text.isdigit()]
                
                if numbers:
                    largest_number = max(numbers)
                    print(f"The largest number in the list is: {largest_number}")
                    
                    # Find the <li> element that contains the largest number
                    for item in list_items:
                        if item.text == str(largest_number):
                            item.click()
                            print(f"Clicked the <li> with the largest number: {largest_number}")
                            break
                else:
                    print("No valid numbers found in the list.")

                break  # Exit the loop after handling the Buy Now button
            
        except Exception as e:
            # Handle errors like element not found or other issues
            print(f"Waiting for the button...{e}")
            # After the exception, refresh the page to retry
            refresh_interval = random.randint(min_refresh_interval, max_refresh_interval)
            print(f"Refreshing the page in {refresh_interval} seconds...")
            time.sleep(refresh_interval)
            driver.refresh()

            # Optional: Break the loop if a certain amount of time has passed (to avoid infinite loop)
            if time.time() - start_time > timeout:
                print("Timed out waiting for the button.")
                break
    
    buy_now_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='buy-now-button']"))
    )
    buy_now_button.click()
    
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.ID, 'buy-now-iframe')))  # Replace with the iframe's identifier
    driver.switch_to.frame(iframe)
    order_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='placeOrderButton']"))
    )
    order_button.click()
    
    cvv_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='enter-cvv']"))
    )
    cvv_button.send_keys("172")
    
    confirm_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='confirm-button']"))
    )
    
    if args.test == True:
        print("Test ORDERED")
    else:
        print("REALLY ORDERED")
        confirm_button.click()
    
    driver.quit()
    
if __name__ == "__main__":
    args = parse_arguents()
    store = args.store
    
    match store:
        case "target":
            print(f"opening target link {args.link}")
            target(args.link, spending_limit, quantity_to_order)
        case "bestbuy":
            bestbuy_paypal(args.link, spending_limit, quantity_to_order)
