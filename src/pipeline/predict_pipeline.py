import os
import sys

import pandas as pd

from src.exception import CustomException
from src.utils import load_object
from src.constants import NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS

class PredictPipeline:

    def __init__(self):
        pass

    def predict(self, features):
        
        try:
            model_path          = os.path.join("artifacts", "model.pkl")
            preprocessor_path   = os.path.join("artifacts", "preprocessor.pkl")

            model         = load_object(file_path=model_path)
            preprocessor  = load_object(file_path=preprocessor_path)

            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)

            return pred
        
        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(
            self,
            gender: str,
            race_ethnicity: str,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_a_data_frame(self):
        try:
            all_columns = CATEGORICAL_COLUMNS + NUMERICAL_COLUMNS
            custom_data_input_dict = {
            col: [getattr(self, col)] for col in all_columns
            }
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e,sys)