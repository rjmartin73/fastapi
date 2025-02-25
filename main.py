from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd

app = FastAPI()

class Item(BaseModel):
    KeyID: int
    Description: str

@app.post("/classify")
async def classify_item(items: List[Item]):
    try:
        # Convert list of objects to DataFrame
        df = pd.DataFrame([item.dict() for item in items])

        # Example classification logic (replace with yours)
        df["MainCategory"] = df["Description"].apply(lambda x: "CONDUIT" if "conduit" in x.lower() else "WIRE")

        return {"data": df.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
