"""
InventoryPage — Page Object for the Sauce Demo product listing.

Selectors sourced from DOM_REFERENCE.md §1 — Inventory Page Selectors.
Contains NO assertions (rule #3 from AGENT_CONTEXT).
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates locators and actions for the inventory / products page."""

    # ── Selectors (exact data-test attributes from DOM_REFERENCE.md) ──
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    ADD_BACKPACK = '[data-test="add-to-cart-sauce-labs-backpack"]'
    ADD_BIKE_LIGHT = '[data-test="add-to-cart-sauce-labs-bike-light"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    CART_LINK = '[data-test="shopping-cart-link"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ──

    def add_backpack_to_cart(self) -> None:
        """Click 'Add to cart' for the Sauce Labs Backpack."""
        self.locator(self.ADD_BACKPACK).click()

    def add_bike_light_to_cart(self) -> None:
        """Click 'Add to cart' for the Sauce Labs Bike Light."""
        self.locator(self.ADD_BIKE_LIGHT).click()

    def go_to_cart(self) -> None:
        """Click the shopping cart icon to navigate to the cart page."""
        self.locator(self.CART_LINK).click()

    # ── Locator accessors for web-first expects ──

    def inventory_container_locator(self):
        """Return the inventory container locator."""
        return self.locator(self.INVENTORY_CONTAINER)

    def cart_badge_locator(self):
        """Return the cart badge locator."""
        return self.locator(self.CART_BADGE)
