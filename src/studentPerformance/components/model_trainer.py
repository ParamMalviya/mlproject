import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from xgboost import XGBRFRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

from studentPerformance.exception import CustomException
from studentPerformance.logger import logger
from studentPerformance.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            
            logger.info("Spliting into training and test set")
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                "RandomForest"     : RandomForestRegressor(),
                "DecisionTree"     : DecisionTreeRegressor(),
                "AdaBoost"         : AdaBoostRegressor(),
                "LinearRegression" : LinearRegression(),
                "Xgboost"          : XGBRFRegressor(),
                "GradientBoosting" : GradientBoostingRegressor(),
                "CatBoosting"      : CatBoostRegressor(verbose=False)
            }

            params = {
                
                "RandomForest"      : {
                    'criterion'     : ['squared_error', 'absolute_error', 'poisson'],
                    'n_estimators'  : [8,16,32,64,128,256],
                    'max_features'  : ['sqrt', 'log2', None]
                },

                "DecisionTree"      : {
                    'criterion'     : ['squared_error', 'absolute_error', 'poisson'],
                    'splitter'      : ['best','random'],
                    'max_features'  : ['sqrt', 'log2']
                },

                "AdaBoost"          : {
                    'learning_rate' : [0.01, 0.05, 0.1],
                    'loss'          : ['linear', 'square', 'exponential'],
                    'n_estimators'  : [8,16,32,64,128,256]
                },

                "LinearRegression"  : {},

                "Xgboost"           : {
                    'learning_rate' :[.1,.01,.05,.001],
                    'n_estimators'  : [8,16,32,64,128,256]
                },

                "GradientBoosting"  : {
                    'n_estimators'  : [8,16,32,64,128,256],
                    'learning_rate' :[.1,.01,.05,.001],
                    'subsample'     :[0.6,0.7,0.75,0.8,0.85,0.9]
                },

                "CatBoosting"       : {
                    'depth'         : [6,8,10],
                    'learning_rate' : [0.01, 0.5, 0.1],
                    'iterations'    : [30, 50, 100]
                }
            }

            model_report: dict = evaluate_models(X_train=x_train, Y_train=y_train, X_test=x_test, Y_test=y_test, models=models, param=params)

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logger.info("Best model found on both training and test dataset")

            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys) from e