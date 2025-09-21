import logger
from fastapi import HTTPException
import asyncio
import serpapi
from backend.models.api_models import Sights, FlightSchedule, HotelDetails

async def run_search(params):
    """Generic function to run SerpAPI searches asynchronously."""
    try:
        # Get API key from params or environment
        return await asyncio.to_thread(lambda: serpapi.search(params))
    except Exception as e:
        logger.exception(f"SerpAPI search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")
