import sys
sys.path.append('')
from fastapi import HTTPException
from typing import List
import asyncio
import serpapi
import os
from backend.models.api_models import Sights, FlightSchedule, HotelDetails, FlightResponse, HotelResponse, SightsResponse
from backend.utils.logger import get_logger
from dotenv import load_dotenv
load_dotenv()

logger = get_logger(__name__)

serpapi_client = serpapi.Client(api_key=os.getenv("SERP_API_KEY"))  # need to export it as export SERP_API_KEY


async def run_search(params):
    """Generic function to run SerpAPI searches asynchronously."""
    try:
        return await asyncio.to_thread(lambda: serpapi_client.search(params).as_dict())
        # return await asyncio.to_thread(serpapi_client.search, params).as_dict()
    except Exception as e:
        logger.exception(f"SerpAPI search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")


async def flight_schedules(flights:FlightSchedule) -> List[FlightResponse]:
    """ Function to call flight api"""
    params = {
              "engine": "google_flights",
              "hl": "en",
              "departure_id": flights.departure_airport_code,
              "arrival_id": flights.arrival_airport_code,
              "outbound_date": flights.outbound_date,
              "return_date": flights.return_date
            }
    search_results = await run_search(params)
    
    if "error" in search_results:  # should Have just returned empty list would be easier while calling it
        logger.error(f"Error getting flights, error - {search_results['error']}")
        return {"error":search_results["error"]}
    
    formatted_flights = []
    best_flights = search_results.get("best_flights", [])
    
    if not best_flights:
        logger.warning("flights fetched is empty")
        return []

    for  details in best_flights:
        if not details.get("flights") or len(details["flights"]) == 0:
            continue

        stops = len(details["flights"])-1

        destination_airport = details.get("flights", [{}])[-1].get("arrival_airport", {}).get("name", "Unknown")
        departure_time = details.get("flights", [{}])[0].get("departure_airport", {}).get("time", "Unknown")
        arrival_time = details.get("flights", [{}])[-1].get("arrival_airport", {}).get("time", "Unknown")


        formatted_flights.append(FlightResponse(
            destination_airport=destination_airport,
            duration=details.get("total_duration",0),
            departure_time=departure_time,
            arrival_time=arrival_time,
            stops=stops,
            price=str(details.get("price", "0"))))  # default price in usd
    
    logger.info(f"Found {len(formatted_flights)} flights")
    return formatted_flights

async def hotel_list(hotel_request:HotelDetails) -> List[HotelResponse]:
    """Function to call hotel api"""
    
    params = {
            "engine": "google_hotels",
            "q": hotel_request.city + " hotels and resorts",
            "check_in_date": hotel_request.check_in_date,
            "check_out_date": hotel_request.check_out_date,
            "hotel_class": hotel_request.hotel_class
            }
    
    search_results = await run_search(params)
    
    if "error" in search_results:
        logger.error(f"Error getting hotels, error - {search_results['error']}")
        return {"error":search_results["error"]}

    hotel_properties = search_results.get("properties", [])
    
    if not hotel_properties:
        logger.warning("no hotels found in search results")
        return []

    formatted_hotels = []
    
    for hotel in hotel_properties:
        formatted_hotels.append(HotelResponse(
            name = hotel.get("name", "Unknown Name"),
            description=hotel.get("description", "unknown description"),
            cost_per_night=hotel.get("rate_per_night",{}).get("lowest", "N/A"),
            rating=hotel.get("overall_rating", 0.0),
            link=hotel.get("link", "N/A")
            ))

    logger.info(f"Found {len(formatted_hotels)} hotels")
    return formatted_hotels

async def tourist_attractions(attractions_request:Sights) -> List[SightsResponse]:
    
    params={
        "engine": "tripadvisor",
        "q": attractions_request.query,
        "ssrc": "A",
    }
    
    search_results = await run_search(params)
    
    if "error" in search_results:
        logger.error(f"Error getting popular destinations, error - {search_results['error']}")
        return {"error":search_results["error"]}
    
    attractions = search_results.get("locations",[])

    if not attractions:
        logger.warning("no attractions found")
        return []

    formatted_attractions = []
    
    for loc in attractions:
        formatted_attractions.append(SightsResponse(
            name=loc.get("title","N/A"),
            description=loc.get("description", "N/A"),
            location=loc.get("location", "Unknown"),
            rating=loc.get("rating", 0.0),
            link=loc.get("link", "N/A")    
        ))
            
    logger.info(f"Found {len(formatted_attractions)} attractions")
    return formatted_attractions