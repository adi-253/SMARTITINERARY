
import sys
sys.path.append('')  # for relative imports

from typing import List, Union, Dict, Any
import asyncio
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
from io import BytesIO
# Use relative imports - cleaner and more maintainable
from models.api_models import FlightResponse, HotelResponse, SightsResponse


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


def download_data(text: str) -> BytesIO:
    """Generates a PDF from the given text and returns a BytesIO buffer."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    
    # Page settings
    page_width = 595.27  # A4 width in points
    page_height = 841.89  # A4 height in points
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    line_height = 14
    
    # Current y position on the page
    y_position = page_height - top_margin
    
    # Split text into lines
    lines = text.split('\n')
    
    for line in lines:
        # Strip markdown-style formatting for PDF (simple approach)
        clean_line = line.strip()
        
        # Check if we need a new page
        if y_position < bottom_margin:
            c.showPage()
            y_position = page_height - top_margin
        
        # Handle headers (markdown style)
        if clean_line.startswith('###'):
            c.setFont("Helvetica-Bold", 11)
            clean_line = clean_line.replace('###', '').strip()
        elif clean_line.startswith('##'):
            c.setFont("Helvetica-Bold", 13)
            clean_line = clean_line.replace('##', '').strip()
        elif clean_line.startswith('#'):
            c.setFont("Helvetica-Bold", 16)
            clean_line = clean_line.replace('#', '').strip()
        elif '**' in clean_line:
            # Handle bold text by removing ** markers and using bold font
            c.setFont("Helvetica-Bold", 10)
            clean_line = clean_line.replace('**', '')
        else:
            c.setFont("Helvetica", 10)
        
        # Handle emoji and special characters (strip them for PDF compatibility)
        clean_line = ''.join(char for char in clean_line if ord(char) < 128 or char.isspace())
        
        # Word wrap for long lines
        max_width = page_width - left_margin - right_margin
        if clean_line:
            # Simple word wrapping
            words = clean_line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + word + ' '
                if c.stringWidth(test_line, c._fontname, c._fontsize) < max_width:
                    current_line = test_line
                else:
                    if current_line:
                        c.drawString(left_margin, y_position, current_line.strip())
                        y_position -= line_height
                        if y_position < bottom_margin:
                            c.showPage()
                            y_position = page_height - top_margin
                    current_line = word + ' '
            
            # Draw remaining text
            if current_line.strip():
                c.drawString(left_margin, y_position, current_line.strip())
                y_position -= line_height
        else:
            # Empty line - just add spacing
            y_position -= line_height / 2
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer