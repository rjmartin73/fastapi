from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from classify import classify_main  # Assuming this is your processing function

app = FastAPI()

SECRET_API_KEY = "c6eb3706-43fc-41a5-b682-e57dcff5feb0"


# ✅ Define JSON request schema
class ItemRequest(BaseModel):
    description: str

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.post("/classify")
async def classify_item(request: ItemRequest, api_key: str = Header(None)):
    # ✅ Check API key
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")

    try:
        # ✅ Pass JSON object to classify_main
        return classify_main(contents=request.description)  

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {e}")
