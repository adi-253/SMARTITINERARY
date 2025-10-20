from pydantic import BaseModel, field_validator, Field
from datetime import date


class Sights(BaseModel):
    """Represents query for trip advisor api."""
    query: str = Field(..., description="What to see, e.g., 'Maldives fun attractions'.")


class FlightSchedule(BaseModel):
    """Flight schedule details."""
    departure_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    arrival_airport_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    outbound_date: str   #YYYY-MM_DD
    return_date: str #YYYY-MM-DD


class HotelDetails(BaseModel):
    """Hotel booking details."""
    city: str
    check_in_date: str # Same as inbound date of flight
    check_out_date: str # Same as outbound date of flight
    hotel_class: str # if multiple classes required can be given like 4,5 with comma separated

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
    stops: int
    departure_time: str  # of first flight
    arrival_time:str    # at the destination
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
    

class RequestResponse(BaseModel):
    """ The request body for the api to take which merges all 3 """
    flight_request: FlightSchedule
    hotel_request: HotelDetails
    sights_request: Sights 

class ItineraryResponse(BaseModel):
    """Final itinerary response"""
    itinerary: str

class PDFRequest(BaseModel):
    itinerary_text: str
