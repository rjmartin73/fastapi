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
async def classify_item(request: Dict):
    try:
        items = request.get("data", [])
        if not isinstance(items, list):
            raise HTTPException(status_code=400, detail="Invalid input: Expected a list of dictionaries")

        # Convert to DataFrame
        df = pd.DataFrame(items)

        # Your classification logic...
        df["MainCategory"] = df["Description"].apply(lambda x: "CONDUIT" if "conduit" in x.lower() else "WIRE")

        return {"data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
