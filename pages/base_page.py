"""
BasePage — shared navigation and wait helpers for all Page Objects.

Contains NO assertions (rule #3 from AGENT_CONTEXT).
"""

from playwright.sync_api import Page


class BasePage:
    """Base class for every Page Object in the framework."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ──

    def navigate(self, path: str = "/") -> None:
        """Navigate to a relative path (base_url is set on the context)."""
        self.page.goto(path)

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    # ── Locator helpers ──

    def locator(self, selector: str):
        """Shorthand for self.page.locator(selector)."""
        return self.page.locator(selector)
