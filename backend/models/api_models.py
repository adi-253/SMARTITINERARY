from pydantic import BaseModel, field_validator, Field
from datetime import date


class Sights(BaseModel):
    """Represents query for trip advisor api."""
    query: str = Field(..., description="What to see, e.g., 'Maldives temples'.")


class FlightSchedule(BaseModel):
    """Flight schedule details."""
    departure_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    arrival_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    outbound_date: str   #YYYY-MM_DD
    return_date: str #YYYY-MM-DD


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

class SightsResponse(BaseModel):
    """The response format for trip advisor api result"""
    name: str
    description: str
    location: str
    rating: float                            
    link: str


class FlightResponse(BaseModel):
    """The Response format for flight api result"""
    destination_airport: str
    duration: int
    stops: str
    price: str  # in usd by default need to add it later
    # airline: str    # this is for immediate airport if stops is not 0
    # aeroplane: str


class HotelResponse(BaseModel):
    """The Response format for Sights api result"""
    name: str
    description: str
    cost_per_night: str
    rating: float
    link: str 
    
