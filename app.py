from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from src.pipeline.predict_pipeline import PredictPipeline, CustomData

app = FastAPI()

# Field names must match src/constants.py (CATEGORICAL_COLUMNS + NUMERICAL_COLUMNS)
class StudentInput(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

@app.get("/")
def index():
    return {"message": "Welcome to the Student Performance Prediction API"}

@app.post("/predict")
def predict_datapoint(input_data: StudentInput):
    data = CustomData(**input_data.model_dump())
    
    pred_df = data.get_data_as_a_data_frame()

    predict_pipeline = PredictPipeline()

    results = predict_pipeline.predict(pred_df)

    return {"Predicted_math_score":float(results[0])}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)