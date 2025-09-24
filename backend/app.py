import sys
sys.path.append('')
import uvicorn
from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(title="Travel Agent")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)