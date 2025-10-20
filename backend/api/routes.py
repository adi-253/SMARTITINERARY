import sys
sys.path.append('')
import asyncio
from fastapi import APIRouter, HTTPException
from models.api_models import RequestResponse
from modules.Service_Api import flight_schedules, hotel_list, tourist_attractions
from modules.helper import format_api_data
from agents.crew_agent import generate_itinerary
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


async def get_complete_iternary(request: RequestResponse):
    """Get data from all services in parallel and format them."""
    try:
        flight_task = asyncio.create_task(flight_schedules(request.flight_request))
        hotel_task = asyncio.create_task(hotel_list(request.hotel_request))
        sights_task = asyncio.create_task(tourist_attractions(request.sights_request))
        
        flights_result, hotel_result, sights_result = await asyncio.gather(flight_task, hotel_task, sights_task)
        
        # Initialize all details as empty lists
        flight_details = []
        hotel_details = []
        sights_details = []
        
        # Format flight details
        if not (isinstance(flights_result, dict) and "error" in flights_result):
            flight_details = flights_result
        flight_text = format_api_data("flights", flight_details)
        
        # Format hotel details
        if not (isinstance(hotel_result, dict) and "error" in hotel_result):
            hotel_details = hotel_result
        hotel_text = format_api_data("hotels", hotel_details)
        
        # Format sights details
        if not (isinstance(sights_result, dict) and "error" in sights_result):
            sights_details = sights_result
        sights_text = format_api_data("attractions", sights_details)
        
        return {
            "flight_text": flight_text,
            "hotel_text": hotel_text,
            "sights_text": sights_text
        }
        
    except Exception as e:
        logger.exception("Error getting complete itinerary")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plan-itinerary")
async def plan_itinerary(request: RequestResponse):
    """Create a complete travel itinerary based on user preferences."""
    try:
        # Get all the data from various services
        data = await get_complete_iternary(request)
        
        # Check if we have any flights and hotels in the text
        if "No flights information available" in data["flight_text"] or "No hotels information available" in data["hotel_text"]:
            raise HTTPException(
                status_code=400, 
                detail="No flights or hotels found for the given criteria"
            )
        
        # Generate detailed itinerary using the AI agent
        itinerary = await generate_itinerary(
            must_visit_locations=data["sights_text"],
            flights_text=data["flight_text"],
            hotels_text=data["hotel_text"],
            check_in_date=request.hotel_request.check_in_date,
            check_out_date=request.hotel_request.check_out_date
        )
        
        return {
            "itinerary": itinerary
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Error planning itinerary")
        raise HTTPException(status_code=500, detail=str(e))   