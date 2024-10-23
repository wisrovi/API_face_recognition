import uvicorn
import multiprocessing

from apis.face_recogniion.api_fr import app


# The main block to run the FastAPI application
if __name__ == "__main__":
    uvicorn_options = {
        "host": "0.0.0.0",
        "port": 1722,
        # "workers": multiprocessing.cpu_count() * 2
        # + 1,  # Make sure there are enough workers
    }

    uvicorn.run(app, **uvicorn_options)
