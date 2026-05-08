# Test Cases — AdNabuTestStore
Application: https://adnabuteststore.myshopify.com  
**Store Password:** AdNabuQA  
**Prepared by:** QA Engineer  


## a) Product Search — 6 Test Cases

---

### TC-S-01 | Search with a Valid Product Name
**Type:** Positive  
**Precondition:** Store is unlocked; user is on the homepage  

**Steps:**
- Navigate to the homepage
- Click the search icon in the header
- Type a known product name (e.g., "Snowboard") into the search input
- Press Enter

Expected Result:
- Search results page loads at `/search?q=Snowboard`
- At least one product matching the query is displayed
- Each result shows a product image, name, and price

---
TC-S-02 | Search Using a Partial/Keyword Match
**Type:** Positive  
**Precondition:** Store is unlocked; user is on the homepage

**Steps:**
- Open the search input
- Type a partial word (e.g., "snow")
- Press Enter

**Expected Result:**
- Results page displays all products whose title or description contains "snow"
- Results are relevant; no error or blank page appears

---

### TC-S-03 | Clicking a Search Result Opens the Correct Product Page
**Type:** Positive  
**Precondition:** A search has been performed returning at least one result

**Steps:**
- Perform a search returning multiple results
- Note the name of the first product shown
- Click on that product

**Expected Result:**
- Browser navigates to the product detail page (`/products/<handle>`)
- Page title/heading matches the product name that was clicked
- Product image, price, and "Add to Cart" button are all visible

---

### TC-S-04 | Search for a Non-Existent Product
**Type:** Negative  
**Precondition:** Store is unlocked; user is on the homepage

**Steps:**
- Open the search input
- Type a string that matches no product (e.g., "xyznonexistent999")
- Press Enter

**Expected Result:**
- Results page loads without error
- A "no results" or "Your search for 'xyznonexistent999' did not return any results" message is displayed
- No products are shown; page does not crash or throw a 500 error

---

### TC-S-05 | Submit Empty Search
**Type:** Negative  
**Precondition:** Store is unlocked; user is on the homepage

**Steps:**
- Click the search icon to open the search input
- Leave the field blank
- Press Enter or click the search submit button

**Expected Result:**
- Either: a validation message prompts the user to enter a search term, **or**
- The store shows all products / a default results page
- Under no circumstance should an unhandled error page appear

---

### TC-S-06 | Search Input with Special Characters (XSS Probe)
**Type:** Edge Case  
**Precondition:** Store is unlocked; user is on the homepage

**Steps:**
- Open the search input
- Type `<script>alert('xss')</script>` and press Enter

**Expected Result:**
- No JavaScript alert executes in the browser
- The input is HTML-escaped and displayed safely in the "no results" message (e.g., shown as literal text)
- Page remains stable; no server error is returned

---

## b) Add to Cart — 6 Test Cases

---

### TC-C-01 | Add a Single In-Stock Product to Cart
**Type:** Positive  
**Precondition:** User is on a product detail page for an in-stock product

**Steps:**
- Navigate to any product detail page
- If variant selectors (size/colour) are present, select a valid option
- Click "Add to cart"

**Expected Result:**
- A cart notification drawer/toast appears confirming the item was added
- The cart icon counter in the header increments by 1
- The cart contains the correct product with the correct price

---

### TC-C-02 | Add a Product and Verify Cart Total Updates
**Type:** Positive  
**Precondition:** Cart is empty; user is on a product detail page

**Steps:**
- Note the product's unit price on the product page
- Click "Add to cart"
- Open the cart (click cart icon or "View cart")

**Expected Result:**
- Cart shows the product with quantity = 1
- Cart subtotal equals the unit price of the product
- Checkout button is visible and active

---

### TC-C-03 | Add the Same Product Twice — Quantity Increments
**Type:** Positive  
**Precondition:** User is on a product detail page

**Steps:**
- Click "Add to cart"
- Without navigating away, click "Add to cart" again (or go back and add once more)
- Open the cart

**Expected Result:**
- The product appears once in the cart with quantity = 2 (not as two separate line items)
- Subtotal reflects unit price × 2

---

### TC-C-04 | Attempt to Add Product Without Selecting a Required Variant
**Type:** Negative  
**Precondition:** A product with required variant options (e.g., Size or Colour) exists

**Steps:**
- Navigate to a product that has size/colour variant selectors
- Do NOT select any variant
- Click "Add to cart"

**Expected Result:**
- An inline validation message appears prompting the user to select a required option (e.g., "Please select a size")
- The product is NOT added to the cart
- Cart counter remains unchanged

---

### TC-C-05 | Set Quantity to 0 Before Adding to Cart
**Type:** Edge Case  
**Precondition:** User is on a product detail page with a quantity input field

**Steps:**
- Clear the quantity field and manually type `0`
- Click "Add to cart"

**Expected Result:**
- Either: the quantity is reset to 1 automatically by the browser/store, **or**
- A validation error is shown ("Quantity must be at least 1")
- Under no circumstance is a product added with quantity 0 or a negative quantity

---

### TC-C-06 | Cart Persists After Browser Page Refresh
**Type:** Negative / Regression  
**Precondition:** At least one product has been added to the cart

**Steps:**
- Add a product to the cart
- Confirm the cart counter shows 1
- Press F5 / reload the page

**Expected Result:**
- After reload, the cart counter still shows 1
- Opening the cart still shows the previously added product with correct quantity and price
- Session/cookie storage is maintained correctly across the reload

---
