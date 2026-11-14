"""
test_booking_negative.py — Negative & unauthorized API tests for Restful-Booker API.

Tests authentication guards (403 Forbidden), non-existent resources (404),
and invalid payload handling.
"""

import pytest


@pytest.mark.api
class TestBookingNegative:
    """Negative and authorization tests."""

    def test_update_booking_without_token_returns_403(self, booking_client, created_booking):
        """
        Verify PUT /booking/{id} without an auth token returns HTTP 403 Forbidden.
        """
        booking_id = created_booking["bookingid"]
        update_payload = {
            "firstname": "Hacker",
            "lastname": "Attempt",
            "totalprice": 999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
        }

        response = booking_client.update_booking(
            booking_id, update_payload, token=None
        )
        assert response.status_code == 403, (
            f"Expected 403 Forbidden without token, got {response.status_code}: {response.text}"
        )

    def test_update_booking_with_invalid_token_returns_403(self, booking_client, created_booking):
        """
        Verify PUT /booking/{id} with an invalid token returns HTTP 403 Forbidden.
        """
        booking_id = created_booking["bookingid"]
        update_payload = {
            "firstname": "InvalidTokenUser",
            "lastname": "Attempt",
            "totalprice": 999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
        }

        response = booking_client.update_booking(
            booking_id, update_payload, token="fake_unauthorized_token_xyz"
        )
        assert response.status_code == 403, (
            f"Expected 403 Forbidden with invalid token, got {response.status_code}: {response.text}"
        )

    def test_partial_update_without_token_returns_403(self, booking_client, created_booking):
        """
        Verify PATCH /booking/{id} without an auth token returns HTTP 403 Forbidden.
        """
        booking_id = created_booking["bookingid"]
        patch_payload = {"firstname": "UnauthorizedPatch"}

        response = booking_client.partial_update_booking(
            booking_id, patch_payload, token=None
        )
        assert response.status_code == 403, (
            f"Expected 403 Forbidden, got {response.status_code}"
        )

    def test_delete_booking_without_token_returns_403(self, booking_client, created_booking):
        """
        Verify DELETE /booking/{id} without an auth token returns HTTP 403 Forbidden.
        """
        booking_id = created_booking["bookingid"]

        response = booking_client.delete_booking(booking_id, token=None)
        assert response.status_code == 403, (
            f"Expected 403 Forbidden without token, got {response.status_code}: {response.text}"
        )

    def test_delete_booking_with_invalid_token_returns_403(self, booking_client, created_booking):
        """
        Verify DELETE /booking/{id} with an invalid token returns HTTP 403 Forbidden.
        """
        booking_id = created_booking["bookingid"]

        response = booking_client.delete_booking(booking_id, token="bad_token_99999")
        assert response.status_code == 403, (
            f"Expected 403 Forbidden with invalid token, got {response.status_code}: {response.text}"
        )

    def test_get_nonexistent_booking_returns_404(self, booking_client):
        """
        Verify GET /booking/{invalid_id} returns HTTP 404 Not Found.
        """
        non_existent_id = 999999999
        response = booking_client.get_booking(non_existent_id)
        assert response.status_code == 404, (
            f"Expected 404 Not Found, got {response.status_code}: {response.text}"
        )

    def test_auth_with_invalid_credentials_returns_no_token(self, booking_client):
        """
        Verify POST /auth with wrong credentials returns 'Bad credentials' and no token.
        """
        response = booking_client.session.post(
            f"{booking_client.base_url}/auth",
            json={"username": "wrong_admin", "password": "wrong_password_123"},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" not in data
        assert data.get("reason") == "Bad credentials"
