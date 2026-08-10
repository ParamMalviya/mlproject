from studentPerformance.logger import setup_logging, logger
from studentPerformance.components.data_ingestion import DataIngestion
from studentPerformance.components.data_transformation import DataTransformation
from studentPerformance.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    setup_logging()   # set up logging once, right at the start

    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    modeltrainer.initiate_model_trainer(train_arr, test_arr)