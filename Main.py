from NetworkSecurity.components.Data_Ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.entity.config_entity import DataIngestionConfig


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
        print(dataingestionartifact)

        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
