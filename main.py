from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from classify import classify_main

app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


@app.post("/classify")
async def classify_item(file: UploadFile = File(...)):
    try:
        # Read JSON file
        contents = await file.read()
        return classify_main(contents=contents)        
        
        # classify_main(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
    
