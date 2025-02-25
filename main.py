from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from classify import classify_main  # Import your original classification function

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
        # Convert Pydantic objects to a list of dictionaries
        items_list = [item.dict() for item in request_body.data]
        
        # Convert to DataFrame
        df = pd.DataFrame(items_list)

        # Pass DataFrame to classification function
        classified_df = classify_main(df)

        # Convert classified DataFrame back to JSON
        return {"data": classified_df}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
