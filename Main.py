from NetworkSecurity.components.Data_Ingestion import DataIngestion
from NetworkSecurity.components.Data_Validation import DataValidation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig


import os
import sys
from datetime import datetime

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info(f"initiate data ingestion config")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"data ingestion completed successfully")
        print(dataingestionartifact)
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, datavalidationconfig)
        logging.info(f"initiate data validation config")
        datavalidationartifact = data_validation.initiate_data_validation()
        print(datavalidationartifact)

        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
