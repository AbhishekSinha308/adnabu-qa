
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL       = "https://adnabuteststore.myshopify.com"
STORE_PASSWORD = "AdNabuQA"
SEARCH_TERM    = "Snowboard"   # A product known to exist in AdNabuTestStore
TIMEOUT        = 20            # seconds for every explicit wait

class Selectors:
    PASSWORD_INPUT  = (By.ID, "Password")
    PASSWORD_SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_TOGGLE   = (By.CSS_SELECTOR, "details[id='Details-menu-drawer-container'] ~ * .header__icon--search, "
                                        ".header__icon--search")
    SEARCH_INPUT    = (By.CSS_SELECTOR, "input[type='search'][name='q'], input[name='q']")
    FIRST_PRODUCT   = (By.CSS_SELECTOR, "ul.grid.product-grid li:first-child a.full-unstyled-link, "
                                        ".product-grid .card-wrapper a.full-unstyled-link")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[name='add'][type='submit'], "
                                        "button#ProductSubmitButton, "
                                        ".product-form__submit")

    CART_NOTIFICATION = (By.CSS_SELECTOR, "cart-notification, #cart-notification")
    CART_COUNT_BADGE  = (By.CSS_SELECTOR, ".cart-count-bubble span[aria-hidden='true']")


class AdNabuStore:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait   = WebDriverWait(driver, TIMEOUT)

    def open(self) -> None:
        self.driver.get(BASE_URL)

    def unlock_password_gate(self) -> None:
        try:
            pwd_input = WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(Selectors.PASSWORD_INPUT)
            )
            pwd_input.clear()
            pwd_input.send_keys(STORE_PASSWORD)
            self.driver.find_element(*Selectors.PASSWORD_SUBMIT).click()
            # Wait until we're past the password gate (URL no longer /password)
            self.wait.until(EC.url_contains(BASE_URL))
        except Exception:
            pass  

    def click_search_icon(self) -> None:
        toggle = self.wait.until(
            EC.element_to_be_clickable(Selectors.SEARCH_TOGGLE)
        )
        toggle.click()

    def type_and_submit_search(self, term: str) -> None:
        search_input = self.wait.until(
            EC.visibility_of_element_located(Selectors.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(term)
        search_input.send_keys(Keys.RETURN)

    def click_first_result(self) -> str:
        first = self.wait.until(
            EC.element_to_be_clickable(Selectors.FIRST_PRODUCT)
        )
        label = first.get_attribute("aria-label") or first.text or SEARCH_TERM
        first.click()
        return label.strip()
    def wait_for_product_page(self) -> None:
        """Block until the URL confirms we are on a /products/ page."""
        self.wait.until(EC.url_contains("/products/"))

    def add_to_cart(self) -> None:
        """Click the Add-to-Cart button."""
        btn = self.wait.until(
            EC.element_to_be_clickable(Selectors.ADD_TO_CART_BTN)
        )
        btn.click()

    def cart_notification_visible(self) -> bool:
        """Return True if Dawn's cart-notification element appears."""
        try:
            self.wait.until(
                EC.visibility_of_element_located(Selectors.CART_NOTIFICATION)
            )
            return True
        except Exception:
            return False

    def cart_count(self) -> int:
        """Read the numeric badge from the cart icon in the header."""
        try:
            badge = self.wait.until(
                EC.visibility_of_element_located(Selectors.CART_COUNT_BADGE)
            )
            return int(badge.text.strip())
        except Exception:
            return 0
class TestSearchAndAddToCart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1440,900")
        options.add_argument("--disable-gpu")

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        cls.store = AdNabuStore(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_search_product_and_add_to_cart(self):
  
        self.store.open()
        self.store.unlock_password_gate()
        self.store.click_search_icon()
        self.store.type_and_submit_search(SEARCH_TERM)
        product_label = self.store.click_first_result()
        print(f"\n  [INFO] Clicked product: '{product_label}'")
        self.store.wait_for_product_page()
        self.store.add_to_cart()
        notification = self.store.cart_notification_visible()
        count        = self.store.cart_count()

        print(f"  [INFO] Cart notification visible : {notification}")
        print(f"  [INFO] Cart count badge          : {count}")

        self.assertTrue(
            notification or count > 0,
            "FAIL — Expected either a cart notification or cart count > 0 after adding product. "
            "Neither condition was met. Check selectors or store availability."
        )
if __name__ == "__main__":
    unittest.main(verbosity=2)
