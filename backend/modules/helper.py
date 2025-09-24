
import sys
sys.path.append('')  # for relative imports

from typing import List, Union, Dict, Any
import asyncio

# Use relative imports - cleaner and more maintainable
from backend.models.api_models import FlightResponse, HotelResponse, SightsResponse


def format_api_data(data_type: str, data: Union[List[Union[FlightResponse, HotelResponse, SightsResponse]], Dict[str, Any]]) -> str:
    """
    Format API data into a readable text format.
    
    Args:
        data_type: Type of data to format ('flights', 'hotels', or 'attractions')
        data: List of API response objects or error dictionary
        
    Returns:
        Formatted text representation of the data
    """
    # Handle error responses
    if isinstance(data, dict) and "error" in data:
        return f"❌ **Error retrieving {data_type}**: {data['error']}"
    
    # Handle empty data
    if not data:
        return f"ℹ️ No {data_type} information available."

    if data_type == "flights":
        formatted_text = "✈️ **Available Flight Options**:\n\n"
        for i, flight in enumerate(data):
            formatted_text += (
                f"**Flight {i + 1}:**\n"
                f"🛬 **Destination:** {flight.destination_airport}\n"
                f"⏱️ **Duration:** {flight.duration} minutes\n"
                f"🛑 **Stops:** {flight.stops}\n"
                f"🕔 **Departure:** {flight.departure_time}\n"
                f"🕖 **Arrival:** {flight.arrival_time}\n"
                f"💰 **Price:** ${flight.price}\n\n"
            )
    
    elif data_type == "hotels":
        formatted_text = "🏨 **Available Hotel Options**:\n\n"
        for i, hotel in enumerate(data):
            formatted_text += (
                f"**Hotel {i + 1}:**\n"
                f"🏨 **Name:** {hotel.name}\n"
                f"📝 **Description:** {hotel.description[:100]}{'...' if len(hotel.description) > 100 else ''}\n"
                f"💰 **Cost per night:** ${hotel.cost_per_night}\n"
                f"⭐ **Rating:** {hotel.rating}\n"
                f"🔗 **More Info:** [Link]({hotel.link})\n\n"
            )
    
    elif data_type == "attractions":
        formatted_text = "🗿 **Available Tourist Attractions**:\n\n"
        for i, sight in enumerate(data):
            formatted_text += (
                f"**Attraction {i + 1}:**\n"
                f"🏛️ **Name:** {sight.name}\n"
                f"📝 **Description:** {sight.description[:100]}{'...' if len(sight.description) > 100 else ''}\n"
                f"📍 **Location:** {sight.location}\n"
                f"⭐ **Rating:** {sight.rating}\n"
                f"🔗 **More Info:** [Link]({sight.link})\n\n"
            )
    
    else:
        return "❌ Invalid data type. Supported types: 'flights', 'hotels', 'attractions'."

    return formatted_text.strip()


