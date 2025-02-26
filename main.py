from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import classify

app = FastAPI(
    title="Classification API",
    description="This API classifies electrical materials into categories such as Conduit, Wire, and Exclude,\nAssigns a conduit or wire type and the diameter or gauge.",
    version="1.0.0"
)


class Item(BaseModel):
    KeyID: int
    Description: str

@app.post("/classify")
async def classify_item(items: List[Item]):
    try:
        # Convert list of objects to DataFrame
        df = pd.DataFrame([item.model_dump() for item in items])

        return classify.classify_main(df)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
