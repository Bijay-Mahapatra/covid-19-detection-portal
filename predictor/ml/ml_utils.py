import pandas as pd
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def load_and_preprocess_data():
    """
    Load and preprocess the COVID dataset.
    Returns: Preprocessed DataFrame
    """
    try:
        dataset_path = os.path.join(settings.BASE_DIR, 'Covid_dataset.csv')
        if not os.path.exists(dataset_path):
            logger.error(f"Dataset file not found at: {dataset_path}")
            raise FileNotFoundError(f"Dataset file not found at: {dataset_path}")
        
        df = pd.read_csv(dataset_path)
        logger.debug(f"Dataset loaded with shape: {df.shape}")
        
        # Map categorical values to numerical
        mappings = {'No': 0, 'Yes': 1}
        columns_to_map = [
            'Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Running Nose',
            'Asthma', 'Headache', 'Heart Disease', 'Diabetes', 'Hyper Tension',
            'Abroad travel', 'Contact with COVID Patient', 'Attended Large Gathering',
            'Visited Public Exposed Places', 'Family working in Public Exposed Places'
        ]
        
        for column in columns_to_map:
            if column in df.columns:
                df[column] = df[column].map(mappings)
            else:
                logger.warning(f"Column {column} not found in dataset")
        
        # Ensure target column exists
        if 'COVID-19' not in df.columns:
            logger.error("Target column 'COVID-19' not found in dataset")
            raise ValueError("Target column 'COVID-19' not found in dataset")
        
        return df
    
    except Exception as e:
        logger.error(f"Error in data preprocessing: {str(e)}")
        raise