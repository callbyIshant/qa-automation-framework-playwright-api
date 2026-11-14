"""
test_auth.py — Authentication tests for Sauce Demo.

Covers:
  • Positive login with standard_user
  • Parametrized negative login (locked_out_user, invalid password)

All selectors come from Page Objects; credentials from config/settings.py.
"""

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import VALID_USER, LOCKED_USER, PASSWORD


@pytest.mark.ui
class TestAuth:
    """Authentication suite for saucedemo.com."""

    def test_valid_login_redirects_to_inventory(self, page):
        """Standard user logs in successfully and sees the inventory page."""
        login = LoginPage(page)
        login.navigate()
        login.login(VALID_USER, PASSWORD)

        inventory = InventoryPage(page)
        expect(inventory.inventory_container_locator()).to_be_visible()

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            pytest.param(
                "locked_out_user",
                "secret_sauce",
                "Epic sadface: Sorry, this user has been locked out.",
                id="locked_out_user",
            ),
            pytest.param(
                "standard_user",
                "wrong_password",
                "Epic sadface: Username and password do not match any user in this service",
                id="invalid_password",
            ),
        ],
    )
    def test_negative_login_shows_error(
        self, page, username, password, expected_error
    ):
        """Invalid credentials display the correct error banner."""
        login = LoginPage(page)
        login.navigate()
        login.login(username, password)

        error = login.error_message_locator()
        expect(error).to_be_visible()
        expect(error).to_have_text(expected_error)
