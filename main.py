from fastapi import FastAPI, HTTPException, File, UploadFile, Header, Request
from pydantic import BaseModel
from classify import classify_main

app = FastAPI()

SECRET_API_KEY = "c6eb3706-43fc-41a5-b682-e57dcff5feb0"

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


@app.post("/classify")
async def classify_item(request: Request, 
                        file: UploadFile = File(...)
                        ):
    
    headers = dict(request.headers)
    api_key = request.headers.get("x-api-key")
    
    # print("\n📌 Received Headers:", headers, "\n")
    # print(f"📌 Extracted API Key: {api_key}\n")
    
    # if api_key != SECRET_API_KEY:
    #     raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")
    try:
        # Read JSON file
        contents = await file.read()
        return classify_main(contents=contents)        
        
        # classify_main(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")
    
