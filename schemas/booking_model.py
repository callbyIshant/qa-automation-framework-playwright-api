"""
Pydantic models for Restful-Booker API data validation and serialization.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookingDates(BaseModel):
    """Checkin and checkout dates model."""
    model_config = ConfigDict(extra="ignore")

    checkin: str
    checkout: str


class Booking(BaseModel):
    """Booking entity model."""
    model_config = ConfigDict(extra="ignore")

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


class BookingResponse(BaseModel):
    """Response returned by POST /booking."""
    model_config = ConfigDict(extra="ignore")

    bookingid: int
    booking: Booking
