from pydantic import BaseModel, field_validator, Field
from datetime import date


class Destination(BaseModel):
    """Represents a travel destination query."""
    query: str = Field(..., description="What to see, e.g., 'Maldives temples'.")


class FlightSchedule(BaseModel):
    """Flight schedule details."""
    departure_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    arrival_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    outbound_date: date
    inbound_date: date


class HotelDetails(BaseModel):
    """Hotel booking details."""
    check_in_date: date  # Same as inbound date of flight
    check_out_date: date # Same as outbound date of flight
    hotel_class: int = Field(..., ge=2, le=5, description="Hotel class (2-5 stars)")

    @field_validator("hotel_class")
    def validate_hotel_class(cls, v):
        if not 2 <= v <= 5:
            raise ValueError("hotel_class must be between 2 and 5")
        return v