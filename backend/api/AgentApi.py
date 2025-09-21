import logger
from fastapi import HTTPException
import asyncio
from serpapi import GoogleSearch
from backend.models.api_models import Sights, FlightSchedule, HotelDetails

async def run_search(params):
    """Generic function to run SerpAPI searches asynchronously."""
    try:
        return await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())
    except Exception as e:
        logger.exception(f"SerpAPI search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")
