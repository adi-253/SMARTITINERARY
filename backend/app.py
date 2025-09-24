import sys
sys.path.append('')
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router

app = FastAPI(title="Travel Agent")

# CORS configuration so the standalone static frontend (opened via file:// or another port) can call the API.
# 405 Method Not Allowed was likely from a blocked OPTIONS preflight for application/json POST.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # In production, restrict this to specific origins (e.g., http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)