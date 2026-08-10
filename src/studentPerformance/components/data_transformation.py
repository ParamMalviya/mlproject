import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from studentPerformance.exception import CustomException
from studentPerformance.logger import logger
from studentPerformance.utils import save_object
from studentPerformance.constants import TARGET_COLUMN, NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        '''
        This Function is responsible for data transformation
        '''
        try:
            numerical_columns = NUMERICAL_COLUMNS
            categorical_columns = CATEGORICAL_COLUMNS

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("OHE", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logger.info(f"Categorical columns: {categorical_columns}")
            logger.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_columns),
                ("cat_pipeline", cat_pipeline, categorical_columns)
            ])
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logger.info("Read train and test data complete")

            logger.info("Obtaining Preprocessor object")
            preprocessing_obj = self.get_data_transformation_object()

            #target column
            target_column_name = TARGET_COLUMN

            #Separate X and y for train and test
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            #Apply preprocessing 
            input_feature_train_df_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_df_arr = preprocessing_obj.transform(input_feature_test_df)

            #Combine X and y back together:
            train_arr = np.c_[input_feature_train_df_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_df_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e, sys) from e