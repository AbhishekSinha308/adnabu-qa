# AdNabuTestStore — QA Assignment Submission

**Store URL:** https://adnabuteststore.myshopify.com  
**Store Password:** AdNabuQA  
**Theme:** Shopify Dawn (default)

---

## Repository Structure

```
adnabu-qa/
├── docs/
│   └── TEST_CASES.md                    # Task 1 — 12 manual test cases
├── tests/
│   └── test_search_and_add_to_cart.py   # Task 2 — Selenium automation
├── reports/
│   └── test_report.txt                  # Test run output (run script to regenerate)
├── requirements.txt
└── README.md
```

---

## Task 1 — Test Cases

See [`docs/TEST_CASES.md`](docs/TEST_CASES.md)

| Section | Test Cases | Coverage |
|---|---|---|
| Product Search | TC-S-01 to TC-S-06 | 3 positive · 2 negative · 1 edge case |
| Add to Cart | TC-C-01 to TC-C-06 | 3 positive · 2 negative · 1 edge case |

---

## Task 2 — Automated Test

**Scenario automated:** Search for a product → click first result → add to cart → assert success

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.8 or higher |
| Google Chrome | Latest stable |

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd adnabu-qa

# 2. Create and activate a virtual environment (recommended)
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> `webdriver-manager` automatically downloads the correct ChromeDriver version.  
> No manual ChromeDriver setup is needed.

### Run the test

```bash
python tests/test_search_and_add_to_cart.py
```

### Run with pytest and capture report

```bash
pip install pytest
pytest tests/ -v --tb=short 2>&1 | tee reports/test_report.txt
```

### Run in headed mode (watch the browser)

Remove or comment out this line in `test_search_and_add_to_cart.py`:

```python
# options.add_argument("--headless=new")   ← comment this out
```

---

## Configuration

All tuneable values are at the top of the test file:

| Variable | Default | Purpose |
|---|---|---|
| `BASE_URL` | `https://adnabuteststore.myshopify.com` | Store URL |
| `STORE_PASSWORD` | `AdNabuQA` | Unlocks the password gate |
| `SEARCH_TERM` | `Snowboard` | Product to search for |
| `TIMEOUT` | `20` | Explicit wait timeout in seconds |

---

## Design Decisions

### No hardcoded sleeps
Every wait uses `WebDriverWait` + `expected_conditions`. Examples:
- `EC.element_to_be_clickable` — before clicking search icon or Add to Cart
- `EC.visibility_of_element_located` — before interacting with inputs
- `EC.url_contains("/products/")` — confirms navigation to product page

### Modular `AdNabuStore` helper class
Actions are separated into single-purpose methods:

| Method | Responsibility |
|---|---|
| `open()` | Navigate to the store |
| `unlock_password_gate()` | Handle the Shopify password form |
| `click_search_icon()` | Open the Dawn search modal |
| `type_and_submit_search()` | Type into input and submit |
| `click_first_result()` | Click the first product card in results |
| `wait_for_product_page()` | Guard until URL confirms product page |
| `add_to_cart()` | Click the Add to Cart button |
| `cart_notification_visible()` | Check for Dawn's slide-in cart drawer |
| `cart_count()` | Read the numeric badge from the cart icon |

### Selectors — Shopify Dawn theme
Selectors are taken from the [Dawn theme source](https://github.com/Shopify/dawn):

| Element | Selector |
|---|---|
| Password input | `#Password` |
| Search toggle | `.header__icon--search` |
| Search input | `input[name='q']` |
| Product card link | `ul.grid.product-grid li:first-child a.full-unstyled-link` |
| Add to cart button | `button[name='add'][type='submit']` |
| Cart notification | `cart-notification` (Web Component) |
| Cart badge | `.cart-count-bubble span[aria-hidden='true']` |

### Dual assertion
The test passes if **either** condition is true:
- The `cart-notification` drawer becomes visible, **or**
- The cart count badge shows a number > 0

This makes the test resilient to minor theme differences while still meaningfully asserting success.

---

## Troubleshooting

**`NoSuchElementException` on search toggle**  
The store may use a customised theme. Open the store in Chrome, right-click the search icon → Inspect, and update `Selectors.SEARCH_TOGGLE` in the test file.

**`TimeoutException` on first result**  
The search term may not match any product. Change `SEARCH_TERM` to a product name visible in the store.

**ChromeDriver version mismatch**  
Run `pip install --upgrade webdriver-manager` to get the latest version.
