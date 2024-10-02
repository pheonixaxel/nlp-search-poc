import logging
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import PlainTextResponse
from src.product_repository import ProductRepository
from contextlib import asynccontextmanager

class SearchCommand(BaseModel):
    query: str

# Instantiate product_repository at the module level
product_repository = None

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    global product_repository
    # This code runs during startup
    product_repository = ProductRepository()
    
    # Yield to keep the app running
    yield

    # This code runs during shutdown
    await product_repository.shutdown()

# Create the FastAPI app with the lifespan event manager
app = FastAPI(title="NLP Enabled Search", lifespan=lifespan)

# Logger configuration
logger = logging.getLogger("uvicorn.error")

# Define the /ping endpoint
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    es_status = await product_repository.ping()
    return f"Elasticsearch alive: {es_status}"

# Define the /search endpoint
@app.get("/search")
async def search(cmd: SearchCommand):
    products = await product_repository.search(cmd.query)
    return {'results': products}
