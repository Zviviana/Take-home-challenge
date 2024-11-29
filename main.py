from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from fpdf import FPDF

driver = webdriver.Chrome()
driver.maximize_window()

os.makedirs("screenshots", exist_ok=True)

def take_screenshot(step_name):
    driver.save_screenshot(f"screenshots/{step_name}.png")

class PDFReport(FPDF):
    def add_step(self, title, image_path):
        self.add_page()
        self.set_font("Arial", size=12)
        self.cell(200, 10, txt=title, ln=True, align="C")
        self.image(image_path, x=10, y=20, w=180)

pdf = PDFReport()

def dismiss_cookie_banner():
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='action:accept']"))
        )
        cookie_button.click()
        print("Cookie banner dismissed.")
    except TimeoutException:
        print("No cookie banner found or already dismissed.")

def safe_click(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()

try:
    driver.get("https://www.mercadolibre.com")
    take_screenshot("01_homepage")
    pdf.add_step("Homepage", "screenshots/01_homepage.png")

    dismiss_cookie_banner()

    mexico_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'México')]"))
    )
    safe_click(mexico_link)
    take_screenshot("02_select_mexico")
    pdf.add_step("Select Mexico", "screenshots/02_select_mexico.png")

    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "as_word"))
    )
    search_box.clear()
    search_box.send_keys("playstation 5")
    search_box.submit()
    take_screenshot("03_search_results")
    pdf.add_step("Search Results", "screenshots/03_search_results.png")

    new_filter = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Nuevo')]"))
    )
    safe_click(new_filter)
    take_screenshot("04_filter_condition")
    pdf.add_step("Filter Condition", "screenshots/04_filter_condition.png")

    new_filter = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Distrito Federal')]"))
    )
    safe_click(new_filter)
    take_screenshot("05_filter_condition")
    pdf.add_step("Filter Condition", "screenshots/05_filter_condition.png")

    try:
        sort_dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".andes-dropdown__trigger"))
        )
        safe_click(sort_dropdown)

        highest_price_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@data-key='price_desc']//span[contains(text(), 'Mayor precio')]"))
        )
        safe_click(highest_price_option)

        take_screenshot("06_sort_order")
        pdf.add_step("Sort Order", "screenshots/06_sort_order.png")
        print("Sorted by highest price.")
    except TimeoutException:
        print("Error sorting by highest price.")
        take_screenshot("error_sort_order")

    try:
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
        )[:5]

        print("\nFirst 5 products:")
        for index, product in enumerate(products, start=1):
            try:
                name = product.find_element(By.CSS_SELECTOR, "h2.poly-box.poly-component__title").text
                price = product.find_element(By.CSS_SELECTOR, "div.poly-component__price").text
                print(f"{index}. {name} - ${price}")
                take_screenshot(f"07_product_{index}")
                pdf.add_step(f"Product {index}", f"screenshots/07_product_{index}.png")
            except NoSuchElementException as e:
                print(f"Error retrieving product {index}: {e}")
    except TimeoutException as e:
        print(f"Error extracting products: {e}")
        take_screenshot("error_extract_products")

finally:
    pdf.output("execution_report.pdf")
    driver.quit()
