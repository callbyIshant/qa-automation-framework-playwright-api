"""
CheckoutPage — Page Object for Sauce Demo checkout steps 1 & 2 and the
order-complete screen.

Selectors sourced from DOM_REFERENCE.md §1 — Cart & Checkout Selectors.
Contains NO assertions (rule #3 from AGENT_CONTEXT).
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Encapsulates locators and actions for checkout step-one, step-two,
    and the order-complete pages."""

    # ── Step One: Your Information ──
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'

    # ── Step Two: Overview (price summary) ──
    SUBTOTAL_LABEL = '[data-test="subtotal-label"]'
    TAX_LABEL = '[data-test="tax-label"]'
    TOTAL_LABEL = '[data-test="total-label"]'
    FINISH_BUTTON = '[data-test="finish"]'

    # ── Order Complete ──
    COMPLETE_HEADER = '[data-test="complete-header"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Step One Actions ──

    def fill_shipping_info(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """Fill in the checkout information form."""
        self.locator(self.FIRST_NAME_INPUT).fill(first_name)
        self.locator(self.LAST_NAME_INPUT).fill(last_name)
        self.locator(self.POSTAL_CODE_INPUT).fill(postal_code)

    def click_continue(self) -> None:
        """Submit the information form to proceed to the overview."""
        self.locator(self.CONTINUE_BUTTON).click()

    # ── Step Two Actions & Accessors ──

    def get_subtotal(self) -> float:
        """Parse the item-total dollar amount from 'Item total: $XX.XX'."""
        text = self.locator(self.SUBTOTAL_LABEL).text_content()
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        """Parse the tax dollar amount from 'Tax: $X.XX'."""
        text = self.locator(self.TAX_LABEL).text_content()
        return float(text.split("$")[1])

    def get_total(self) -> float:
        """Parse the total dollar amount from 'Total: $XX.XX'."""
        text = self.locator(self.TOTAL_LABEL).text_content()
        return float(text.split("$")[1])

    def click_finish(self) -> None:
        """Click the Finish button to complete the order."""
        self.locator(self.FINISH_BUTTON).click()

    # ── Order Complete Accessors ──

    def get_complete_header_text(self) -> str:
        """Return the text of the order-complete heading."""
        return self.locator(self.COMPLETE_HEADER).text_content()

    def complete_header_locator(self):
        """Return the complete-header locator for Playwright web-first expects."""
        return self.locator(self.COMPLETE_HEADER)
