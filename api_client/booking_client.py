"""
BookingClient — HTTP client wrapper for restful-booker API.

Endpoints wrapped:
  • POST   /auth           (authenticate)
  • POST   /booking        (create booking)
  • GET    /booking/{id}   (get booking)
  • PUT    /booking/{id}   (update booking)
  • PATCH  /booking/{id}   (partial update booking)
  • DELETE /booking/{id}   (delete booking)
  • GET    /booking        (get all booking IDs)
"""

import requests
from typing import Optional, Dict, Any

from config.settings import API_BASE_URL, API_USERNAME, API_PASSWORD

# Sentinel to distinguish between omitting token and explicitly passing None
_DEFAULT_TOKEN = object()


class BookingClient:
    """Client for interacting with the Restful Booker API."""

    def __init__(self, base_url: str = API_BASE_URL, timeout: int = 15) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.token: Optional[str] = None

    # ── Authentication ──

    def authenticate(
        self,
        username: str = API_USERNAME,
        password: str = API_PASSWORD,
    ) -> str:
        """
        Authenticate with the API and store the auth token.
        POST /auth
        """
        url = f"{self.base_url}/auth"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}

        response = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return self.token

    # ── Booking Endpoints ──

    def create_booking(
        self,
        booking_data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Create a new booking.
        POST /booking
        """
        url = f"{self.base_url}/booking"
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            default_headers.update(headers)

        return self.session.post(
            url,
            json=booking_data,
            headers=default_headers,
            timeout=self.timeout,
        )

    def get_booking(
        self,
        booking_id: int,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Retrieve a booking by ID.
        GET /booking/{id}
        """
        url = f"{self.base_url}/booking/{booking_id}"
        default_headers = {"Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        return self.session.get(
            url,
            headers=default_headers,
            timeout=self.timeout,
        )

    def update_booking(
        self,
        booking_id: int,
        booking_data: Dict[str, Any],
        token: Any = _DEFAULT_TOKEN,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Update an existing booking (full update).
        PUT /booking/{id}
        Requires Cookie: token=<token>
        """
        url = f"{self.base_url}/booking/{booking_id}"
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        auth_token = self.token if token is _DEFAULT_TOKEN else token
        if auth_token:
            default_headers["Cookie"] = f"token={auth_token}"

        if headers:
            default_headers.update(headers)

        return self.session.put(
            url,
            json=booking_data,
            headers=default_headers,
            timeout=self.timeout,
        )

    def partial_update_booking(
        self,
        booking_id: int,
        booking_data: Dict[str, Any],
        token: Any = _DEFAULT_TOKEN,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Partially update an existing booking.
        PATCH /booking/{id}
        """
        url = f"{self.base_url}/booking/{booking_id}"
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        auth_token = self.token if token is _DEFAULT_TOKEN else token
        if auth_token:
            default_headers["Cookie"] = f"token={auth_token}"

        if headers:
            default_headers.update(headers)

        return self.session.patch(
            url,
            json=booking_data,
            headers=default_headers,
            timeout=self.timeout,
        )

    def delete_booking(
        self,
        booking_id: int,
        token: Any = _DEFAULT_TOKEN,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Delete a booking by ID.
        DELETE /booking/{id}
        Requires Cookie: token=<token>
        """
        url = f"{self.base_url}/booking/{booking_id}"
        default_headers: Dict[str, str] = {}
        auth_token = self.token if token is _DEFAULT_TOKEN else token
        if auth_token:
            default_headers["Cookie"] = f"token={auth_token}"

        if headers:
            default_headers.update(headers)

        return self.session.delete(
            url,
            headers=default_headers,
            timeout=self.timeout,
        )

    def get_booking_ids(
        self,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Retrieve a list of all booking IDs, optionally filtered.
        GET /booking
        """
        url = f"{self.base_url}/booking"
        return self.session.get(url, params=params, timeout=self.timeout)
