from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import classify
import json

app = FastAPI(
    title="Classification API",
    description="This API classifies electrical materials into categories such as Conduit, Wire, and Exclude,\nAssigns a conduit or wire type and the diameter or gauge.",
    version="1.0.0"
)


class Item(BaseModel):
    KeyID: int
    Description: str


'''
    Main Method used by the api to classify the items
'''
@app.post("/classify")
async def classify_item(items: List[Item]):
    try:
        # Convert list of objects to DataFrame
        df = pd.DataFrame([item.model_dump() for item in items])

        return classify.classify_main(df)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file\n{e}")


@app.get("/classification-terms")
def get_definitions():
    """Returns lists of wire and conduit terms used to classify """
    return f"Conduit terms: {sorted(list(classify.conduit_terms))}\n\
            Conduit exclusion: {sorted(classify.conduit_exclude_terms)}\n\
            Wire terms: {sorted(list(classify.wire_terms))}\n\
            Wire exclusions: {sorted(classify.wire_exclude_terms)}"


# test data for testing the classifier
test_data = [
    {"KeyID": "1093404", "Description": "white with black stripe 12 sol"},
    {"KeyID": "1102219", "Description": "white with red stripe 12 solid"},
    {"KeyID": "1187083", "Description": "white with blue stripe 12 soli"}
]


# method to test the classifier
def test_classifier(test_data):
    df = pd.DataFrame(test_data)
    return classify.classify_main(df)


pretty_json = json.dumps(test_classifier(test_data), indent=4)
print(pretty_json)

# print(get_definitions())
