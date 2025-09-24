# SmartItinerary

SmartItinerary is an AI-powered travel planning application that automatically generates detailed, personalized travel itineraries based on user preferences. The application combines real-time flight and hotel information with tourist attraction data to create comprehensive day-by-day travel plans.

## 🌟 Features

- 🛫 **Flight Search**: Find available flights between specified airports
- 🏨 **Hotel Recommendations**: Get hotel options based on location, dates, and rating preferences
- 🗿 **Attraction Discovery**: Discover popular tourist attractions at your destination
- 📝 **AI-Generated Itineraries**: Get a complete day-by-day itinerary with all the above information
- 🕒 **Time Management**: Includes recommended visit times and scheduling
- 🍽️ **Restaurant Suggestions**: Incorporates dining recommendations
- 🚗 **Transportation Tips**: Provides local transportation information

## 📋 Project Structure

```
SmartItinerary/
├── backend/                   # Backend FastAPI server
│   ├── agent/                 # Python virtual environment
│   ├── agents/                # AI agent implementation
│   │   ├── crew_agent.py      # CrewAI implementation
│   │   └── llm.py            # LLM model configuration
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── models/
│   │   └── api_models.py     # Pydantic data models
│   ├── modules/
│   │   ├── helper.py         # Helper functions
│   │   └── Service_Api.py    # External API service calls
│   ├── utils/
│   │   └── logger.py         # Logging utilities
│   ├── app.py                # Main FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Simple HTML/CSS/JS frontend
│   ├── index.html            # Main HTML page
│   ├── script.js             # Frontend JavaScript
│   └── styles.css            # CSS styling
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js (optional, only if you plan to enhance the frontend)
- SerpAPI API key (for flight, hotel, and attraction data)
- Gemini API key (for AI-powered itinerary generation)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/SmartItinerary.git
   cd SmartItinerary
   ```

2. **Set up Python virtual environment**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the backend directory with the following:

   ```
   SERP_API_KEY=your_serpapi_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Then export the SERP API key to your environment:

   ```bash
   export SERP_API_KEY=your_serpapi_key_here
   ```

5. **Start the backend server**

   ```bash
   python app.py
   ```

   The API will be available at http://localhost:8000

6. **Open the frontend**
   Simply open `frontend/index.html` in your web browser.


## 🛠️ Technologies Used

- **Backend**:
  - FastAPI (API framework)
  - CrewAI (Agent-based AI orchestration)
  - Gemini API (AI model for itinerary generation)
  - SerpAPI (Data source for flights, hotels, attractions)
  - Pydantic (Data validation)
- **Frontend**:
  - HTML/CSS/JavaScript (Simple frontend interface)

## 🧩 How it Works

1. **Data Collection**: The application fetches flight details, hotel options, and tourist attractions using SerpAPI.
2. **Data Processing**: The data is formatted into a structured format.
3. **AI Processing**: CrewAI agents process the structured data.
4. **Itinerary Generation**: The AI generates a comprehensive itinerary with day-by-day details.
5. **Frontend Display**: The frontend renders the itinerary in a user-friendly format.

## 📝 Notes for Development

- Add error handling for API rate limits
- Implement caching to reduce API calls
- Consider adding user accounts to save itineraries
- Add more customization options (budget, travel style, etc.)

