"""
test_checkout_e2e.py — End-to-end checkout flow with price & tax math.

Flow:
  1. Login as standard_user
  2. Add Sauce Labs Backpack + Bike Light to cart
  3. Navigate to cart → Checkout
  4. Fill shipping info → Continue to overview
  5. Verify:  subtotal + tax == total  (floating-point safe)
  6. Finish order → assert "Thank you for your order!" banner

All selectors come from Page Objects; credentials from config/settings.py.
"""

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import VALID_USER, PASSWORD


@pytest.mark.ui
class TestCheckoutE2E:
    """Full end-to-end checkout with price arithmetic verification."""

    def test_checkout_two_items_with_price_and_tax_math(self, page):
        """Add two products, complete checkout, and verify price math."""

        # ── Step 1: Login ──
        login = LoginPage(page)
        login.navigate()
        login.login(VALID_USER, PASSWORD)

        # ── Step 2: Add items to cart ──
        inventory = InventoryPage(page)
        expect(inventory.inventory_container_locator()).to_be_visible()

        inventory.add_backpack_to_cart()
        inventory.add_bike_light_to_cart()

        # Verify cart badge shows "2"
        expect(inventory.cart_badge_locator()).to_have_text("2")

        # ── Step 3: Go to cart → Checkout ──
        inventory.go_to_cart()

        cart = CartPage(page)
        cart.click_checkout()

        # ── Step 4: Fill shipping info → Continue ──
        checkout = CheckoutPage(page)
        checkout.fill_shipping_info("Jane", "Doe", "90210")
        checkout.click_continue()

        # ── Step 5: Price & tax math verification ──
        subtotal = checkout.get_subtotal()
        tax = checkout.get_tax()
        total = checkout.get_total()

        # Subtotal and tax must be positive
        assert subtotal > 0, f"Subtotal should be positive, got {subtotal}"
        assert tax > 0, f"Tax should be positive, got {tax}"

        # Core math check: subtotal + tax == total (float-safe)
        assert subtotal + tax == pytest.approx(total, abs=0.01), (
            f"Price math failed: {subtotal} + {tax} = {subtotal + tax}, "
            f"but page shows total = {total}"
        )

        # ── Step 6: Finish and verify success ──
        checkout.click_finish()

        expect(checkout.complete_header_locator()).to_be_visible()
        expect(checkout.complete_header_locator()).to_have_text(
            "Thank you for your order!"
        )
