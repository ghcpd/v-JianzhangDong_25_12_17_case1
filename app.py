"""Application entrypoint that runs the FastAPI app with Uvicorn.

This module is the standard script entry used to start the web server
when running locally (python app.py).
"""

from api import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
