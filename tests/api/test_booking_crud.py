"""
test_booking_crud.py — Full CRUD persistence & JSON Schema validation for Restful-Booker API.

Endpoints covered:
  • POST   /booking        (Create)
  • GET    /booking/{id}   (Read)
  • PUT    /booking/{id}   (Update)
  • PATCH  /booking/{id}   (Partial Update)
  • DELETE /booking/{id}   (Delete)
"""

import pytest
from utils.schema_validator import validate_json_schema
from schemas.booking_model import Booking, BookingResponse


@pytest.mark.api
class TestBookingCRUD:
    """CRUD operations and schema validations for bookings."""

    def test_create_booking_schema_and_values(self, booking_client, sample_booking_payload, auth_token):
        """
        Verify POST /booking creates a booking, validates JSON Schema and Pydantic model,
        and returns matching values.
        """
        response = booking_client.create_booking(sample_booking_payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()

        # 1. JSON Schema Validation
        validate_json_schema(data, "booking_response_schema.json")

        # 2. Pydantic Model Validation
        booking_resp_model = BookingResponse.model_validate(data)
        assert booking_resp_model.bookingid > 0

        # 3. Payload integrity check
        booking = data["booking"]
        assert booking["firstname"] == sample_booking_payload["firstname"]
        assert booking["lastname"] == sample_booking_payload["lastname"]
        assert booking["totalprice"] == sample_booking_payload["totalprice"]
        assert booking["depositpaid"] == sample_booking_payload["depositpaid"]
        assert booking["bookingdates"] == sample_booking_payload["bookingdates"]
        assert booking["additionalneeds"] == sample_booking_payload["additionalneeds"]

        # Teardown
        booking_client.delete_booking(data["bookingid"], token=auth_token)

    def test_get_booking_by_id(self, booking_client, created_booking):
        """
        Verify GET /booking/{id} returns the booking details matching the schema.
        """
        booking_id = created_booking["bookingid"]
        response = booking_client.get_booking(booking_id)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()

        # 1. JSON Schema Validation
        validate_json_schema(data, "booking_schema.json")

        # 2. Pydantic Validation
        booking_model = Booking.model_validate(data)
        assert booking_model.firstname == created_booking["booking"]["firstname"]
        assert booking_model.lastname == created_booking["booking"]["lastname"]

    def test_update_booking_put_persistence(self, booking_client, created_booking, auth_token):
        """
        Verify PUT /booking/{id} updates all fields and the changes persist in GET.
        Requires Cookie: token=<token>.
        """
        booking_id = created_booking["bookingid"]
        updated_payload = {
            "firstname": "Jane",
            "lastname": "Smith",
            "totalprice": 300,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-07-01",
                "checkout": "2026-07-15",
            },
            "additionalneeds": "Airport Shuttle",
        }

        # 1. Send PUT request
        put_response = booking_client.update_booking(
            booking_id, updated_payload, token=auth_token
        )
        assert put_response.status_code == 200, f"Expected 200, got {put_response.status_code}: {put_response.text}"
        put_data = put_response.json()

        validate_json_schema(put_data, "booking_schema.json")
        assert put_data["firstname"] == "Jane"
        assert put_data["totalprice"] == 300
        assert put_data["depositpaid"] is False

        # 2. Persistence check: GET must reflect the updated record
        get_response = booking_client.get_booking(booking_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["firstname"] == "Jane"
        assert get_data["lastname"] == "Smith"
        assert get_data["totalprice"] == 300
        assert get_data["depositpaid"] is False
        assert get_data["additionalneeds"] == "Airport Shuttle"

    def test_partial_update_booking_patch_persistence(self, booking_client, created_booking, auth_token):
        """
        Verify PATCH /booking/{id} partially updates fields and changes persist.
        """
        booking_id = created_booking["bookingid"]
        patch_payload = {
            "firstname": "Robert",
            "totalprice": 450,
        }

        patch_response = booking_client.partial_update_booking(
            booking_id, patch_payload, token=auth_token
        )
        assert patch_response.status_code == 200, f"Expected 200, got {patch_response.status_code}"
        patch_data = patch_response.json()

        assert patch_data["firstname"] == "Robert"
        assert patch_data["totalprice"] == 450
        # Untouched fields must retain original values
        assert patch_data["lastname"] == created_booking["booking"]["lastname"]

        # Persistence check
        get_response = booking_client.get_booking(booking_id)
        assert get_response.status_code == 200
        assert get_response.json()["firstname"] == "Robert"
        assert get_response.json()["totalprice"] == 450

    def test_delete_booking_persistence(self, booking_client, sample_booking_payload, auth_token):
        """
        Verify DELETE /booking/{id} removes the booking and returns HTTP 201.
        Subsequent GET must return HTTP 404.
        """
        # Create booking to delete
        create_res = booking_client.create_booking(sample_booking_payload)
        assert create_res.status_code == 200
        booking_id = create_res.json()["bookingid"]

        # Delete booking with valid auth token
        del_response = booking_client.delete_booking(booking_id, token=auth_token)
        assert del_response.status_code == 201, (
            f"Expected HTTP 201 per DOM_REFERENCE.md, got {del_response.status_code}: {del_response.text}"
        )

        # Persistence check: GET must return 404 Not Found
        get_response = booking_client.get_booking(booking_id)
        assert get_response.status_code == 404, f"Expected 404 Not Found, got {get_response.status_code}"

    def test_full_crud_lifecycle(self, booking_client, auth_token):
        """
        End-to-end CRUD lifecycle: Create -> Read -> Update -> Partial Update -> Delete -> Verify 404.
        """
        initial_data = {
            "firstname": "Lifecycle",
            "lastname": "Tester",
            "totalprice": 500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-08-01",
                "checkout": "2026-08-10",
            },
            "additionalneeds": "All-inclusive",
        }

        # 1. CREATE
        create_res = booking_client.create_booking(initial_data)
        assert create_res.status_code == 200
        booking_id = create_res.json()["bookingid"]
        validate_json_schema(create_res.json(), "booking_response_schema.json")

        # 2. READ
        read_res = booking_client.get_booking(booking_id)
        assert read_res.status_code == 200
        validate_json_schema(read_res.json(), "booking_schema.json")
        assert read_res.json()["firstname"] == "Lifecycle"

        # 3. UPDATE (PUT)
        update_data = {
            "firstname": "UpdatedLifecycle",
            "lastname": "Tester",
            "totalprice": 600,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-08-02",
                "checkout": "2026-08-12",
            },
            "additionalneeds": "Spa Access",
        }
        put_res = booking_client.update_booking(booking_id, update_data, token=auth_token)
        assert put_res.status_code == 200
        assert put_res.json()["firstname"] == "UpdatedLifecycle"
        assert put_res.json()["totalprice"] == 600

        # 4. PARTIAL UPDATE (PATCH)
        patch_data = {"additionalneeds": "VIP Lounge"}
        patch_res = booking_client.partial_update_booking(booking_id, patch_data, token=auth_token)
        assert patch_res.status_code == 200
        assert patch_res.json()["additionalneeds"] == "VIP Lounge"

        # 5. DELETE
        del_res = booking_client.delete_booking(booking_id, token=auth_token)
        assert del_res.status_code == 201

        # 6. VERIFY REMOVAL
        verify_res = booking_client.get_booking(booking_id)
        assert verify_res.status_code == 404
