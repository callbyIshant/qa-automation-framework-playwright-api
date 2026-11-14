"""
CartPage — Page Object for the Sauce Demo shopping-cart screen.

Selectors sourced from DOM_REFERENCE.md §1 — Cart & Checkout Selectors.
Contains NO assertions (rule #3 from AGENT_CONTEXT).
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates locators and actions for the shopping-cart page."""

    # ── Selectors (exact data-test attributes from DOM_REFERENCE.md) ──
    CHECKOUT_BUTTON = '[data-test="checkout"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ──

    def click_checkout(self) -> None:
        """Click the Checkout button to begin the checkout flow."""
        self.locator(self.CHECKOUT_BUTTON).click()
