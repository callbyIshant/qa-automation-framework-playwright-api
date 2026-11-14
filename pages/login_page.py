"""
LoginPage — Page Object for https://www.saucedemo.com (login screen).

Selectors sourced from DOM_REFERENCE.md §1 — Login Page Selectors.
Contains NO assertions (rule #3 from AGENT_CONTEXT).
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates locators and actions for the Sauce Demo login page."""

    # ── Selectors (exact data-test attributes from DOM_REFERENCE.md) ──
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ──

    def navigate(self) -> None:
        """Open the login page."""
        super().navigate("/")

    def login(self, username: str, password: str) -> None:
        """Fill credentials and click the login button."""
        self.locator(self.USERNAME_INPUT).fill(username)
        self.locator(self.PASSWORD_INPUT).fill(password)
        self.locator(self.LOGIN_BUTTON).click()

    def get_error_message_text(self) -> str:
        """Return the text content of the error banner."""
        return self.locator(self.ERROR_MESSAGE).text_content()

    def error_message_locator(self):
        """Return the error-message locator for Playwright web-first expects."""
        return self.locator(self.ERROR_MESSAGE)
