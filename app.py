from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from src.pipeline.predict_pipeline import PredictPipeline, CustomData

app = FastAPI()

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
    data = CustomData(
        gender=input_data.gender,
        race_ethnicity=input_data.race_ethnicity,
        parental_level_of_education=input_data.parental_level_of_education,
        lunch=input_data.lunch,
        test_preparation_course=input_data.test_preparation_course,
        reading_score=input_data.reading_score,
        writing_score=input_data.writing_score
    )
    pred_df = data.get_data_as_a_dataframe()

    predict_pipeline = PredictPipeline()

    results = predict_pipeline.predict(pred_df)

    return {"Predicted_math_score":float(results[0])}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)