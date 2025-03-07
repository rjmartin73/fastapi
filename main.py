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
    return f"Conduit terms: {sorted(list(classify.conduit_terms))}\
            Conduit exclusion: {sorted(classify.conduit_exclude_terms)}\
            Wire terms: {sorted(list(classify.wire_terms))}\
            Wire exclusions: {sorted(classify.wire_exclude_terms)}"


# test data for testing the classifier
test_data = [
    {"KeyID": "1093404", "Description": "TRANSFER PVC FROM JXLTG TO FT "},
    {"KeyID": "1102219", "Description": "TRANSFER PVC FROM JXLTG TO FT"},
    {"KeyID": "1187083", "Description": "6 Strand Copper Wire Soft Draw"},
    {"KeyID": "1224745", "Description": "250 Mcm Aluminum Wire"},
    {"KeyID": "1224748", "Description": "[Metallic Flexible Conduit] St"},
    {"KeyID": "1224749", "Description": "Flex Cnnectors"},
    {"KeyID": "1265255", "Description": "WIREWY CLOSE PLT"},
    {"KeyID": "1265263", "Description": "3 Gauge Copper Wire"},
    {"KeyID": "1296901", "Description": "3/0Cooper Wire"},
    {"KeyID": "1309325", "Description": "WIC MCA 12/2 SOL 1000R"},
    {"KeyID": "1309332", "Description": "1/0 Wire Copper"},
    {"KeyID": "1320951", "Description": "INT COND 3/4"},
    {"KeyID": "1333939", "Description": "12/4 MC SOL"},
    {"KeyID": "1343493", "Description": "3/8 FLEX"},
    {"KeyID": "1347172", "Description": "2IN UNIVERSAL RIGID/CONDUIT C"},
    {"KeyID": "1347173", "Description": "PVC 200P 2IN SCH40 PVC CONDUIT"},
    {"KeyID": "1347180", "Description": "WIC MCA 12/2 SOL 1000R"},
    {"KeyID": "1359826", "Description": "2 IN COND HGR STL"},
    {"KeyID": "1359827", "Description": "2-1/2 IN COND HGR STL"},
    {"KeyID": "1413445", "Description": "#8 Wire"},
    {"KeyID": "1413446", "Description": "3/0 Wire"},
    {"KeyID": "1532592", "Description": "SO 12/4 STR"},
    {"KeyID": "1737262", "Description": "#12 Wire"},
    {"KeyID": "1737263", "Description": "#12 Wire"},
    {"KeyID": "1737264", "Description": "#12 Wire"},
    {"KeyID": "1764351", "Description": "500' roll of # 10 awg SOLID GR"},
    {"KeyID": "2151330", "Description": "3'' seal tight flex"},
    {"KeyID": "2245046", "Description": "4/0 copper wire THWN"},
    {"KeyID": "2245047", "Description": "3/0 copper wire THWN"},
    {"KeyID": "2245048", "Description": "#2 cooper wire THWN"},
    {"KeyID": "2406204", "Description": "12' long ceiling grid wire"},
    {"KeyID": "2742982", "Description": "3/8\" FLEXSTEEL CONDUIT"},
    {"KeyID": "2958703", "Description": "#12 Jack chain"},
    {"KeyID": "2958704", "Description": "#12 Jack chain"},
    {"KeyID": "2958706", "Description": "#12 Jack chain"},
    {"KeyID": "3091172", "Description": "2500' roll #12 awg grey wire "},
    {"KeyID": "3091174", "Description": "2500' roll #12 awg orange thh"},
    {"KeyID": "3091175", "Description": "2500' roll #12 awg yellow thh"},
    {"KeyID": "3091177", "Description": "2500' roll #12 awg white wire"},
    {"KeyID": "3091178", "Description": "2500' roll #12 awg white wire"},
    {"KeyID": "3091179", "Description": "2500' roll #12 awg white wire"},
    {"KeyID": "3091180", "Description": "2500' roll #12 awg grey wire "},
    {"KeyID": "3091181", "Description": "2500' roll #12 awg grey wire "},
    {"KeyID": "3091182", "Description": "2500' roll #10 awg white wire"},
    {"KeyID": "3091183", "Description": "2500' roll #10 awg white wire"},
    {"KeyID": "3091184", "Description": "2500' roll #10 awg white wire"},
    {"KeyID": "3091185", "Description": "2500' roll #14 awg purple thh"},
    {"KeyID": "3163554", "Description": "21016-299BO WIRE COST"},
    {"KeyID": "3179956", "Description": "#2 AWG bare stranded"},
    {"KeyID": "3179958", "Description": "#2 copper thhn"},
    {"KeyID": "3179967", "Description": "4/0 copper thhn"},
    {"KeyID": "3783282", "Description": "3-STEEL THINWALL CONDUIT"},
    {"KeyID": "3847973", "Description": "2500' roll of Green #12 awg T"},
    {"KeyID": "3866878", "Description": "2500' roll of Green #12 awg TH"},
    {"KeyID": "3897245", "Description": "2500' roll of Green #12 awg TH"}
]


# method to test the classifier
def test_classifier(test_data):
    df = pd.DataFrame(test_data)
    return classify.classify_main(df)


print(test_classifier(test_data))
# print(get_definitions)
