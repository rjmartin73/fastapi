from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from typing import List
from classify import classify_main

app = FastAPI()

SECRET_API_KEY = "c6eb3706-43fc-41a5-b682-e57dcff5feb0"

class ClassificationRequest(BaseModel):
    KeyID: int
    Description: str

@app.post("/classify")
async def classify_item(request: Request, items: List[ClassificationRequest]):
    
    headers = dict(request.headers)
    api_key = request.headers.get("x-api-key")

    # if api_key != SECRET_API_KEY:
    #     raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")
    
    try:
        results = []
        for item in items:
            classification = classify_main(item.Description)
            results.append({
                "KeyID": item.KeyID,
                "Description": item.Description,
                "MainCategory": classification["MainCategory"],
                "SubCategory": classification["SubCategory"],
                "Size": classification["Size"],
                "FinalLabel": classification["FinalLabel"]
            })

        return {"data": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
