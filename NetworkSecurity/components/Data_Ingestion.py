from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

## configuration of the Data Ingestion config

from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self)->pd.DataFrame:
        """
        export the data from mongodb to the feature store
        """
        try:
            logging.info("exporting the data from mongodb to the feature_store")
            client = pymongo.MongoClient(MONGO_DB_URL)
            logging.info(f"connected to mongodb client: {client}")
            db = client[self.data_ingestion_config.database_name]
            collection = db[self.data_ingestion_config.collection_name]
            logging.info(f"fetching the data from database: {self.data_ingestion_config.database_name} andcollection: {self.data_ingestion_config.collection_name}")
            data = pd.DataFrame(list(collection.find()))
            logging.info(f"Data shape: {data.shape}")
            if "_id" in data.columns:
                data = data.drop(columns=["_id"],axis=1)
                logging.info(f"Data shape after dropping _id column: {data.shape}")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            data.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            logging.info(f"Data saved to feature store: {self.data_ingestion_config.feature_store_file_path}")
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self,data: pd.DataFrame):
        try:
            train_set,test_set = train_test_split(data,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("perform train test split on data")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header= True)
            logging.info(f"export to train and test file path: {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            data = self.export_data_into_feature_store()
            self.split_data_as_train_test(data)
            dataingestionartifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path,test_file_path = self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
    
        except Exception as e:
            raise NetworkSecurityException  
        
     
