from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Define input model
class Item(BaseModel):
    KeyID: int
    Description: str

class RequestBody(BaseModel):
    data: List[Item]  # Expecting "data" key with a list of items

@app.post("/classify")
async def classify_items(request_body: RequestBody):
    try:
        items = request_body.data  # Extract the list from "data"
        
        # Process the data
        results = []
        for item in items:
            result = {
                "KeyID": item.KeyID,
                "Description": item.Description,
                "Category": "WIRE" if "wire" in item.Description.lower() else "CONDUIT"
            }
            results.append(result)

        return {"data": results}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
