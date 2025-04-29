import pandas as pd
import joblib
import os
from django.conf import settings
import logging
from .ml_trainer import train_and_save_model

logger = logging.getLogger(__name__)

def predict_covid(symptoms):
    """
    Predict COVID-19 outcome based on symptoms.
    Args:
        symptoms (dict): Dictionary of symptom values (0 or 1)
    Returns:
        dict: Prediction result, message, risk percentage, and feature importance
    """
    try:
        # Define expected features
        feature_names = [
            'Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Running Nose',
            'Asthma', 'Headache', 'Heart Disease', 'Diabetes', 'Hyper Tension',
            'Abroad travel', 'Contact with COVID Patient', 'Attended Large Gathering',
            'Visited Public Exposed Places', 'Family working in Public Exposed Places'
        ]
        
        # Validate input symptoms
        for feature in feature_names:
            if feature not in symptoms:
                symptoms[feature] = 0
            if symptoms[feature] not in [0, 1]:
                raise ValueError(f"Invalid value for {feature}: {symptoms[feature]}. Must be 0 or 1.")
        
        # Load or train the model
        model_path = os.path.join(settings.BASE_DIR, 'covid_model.joblib')
        if not os.path.exists(model_path):
            logger.info("Model file not found, training new model")
            model, feature_importance = train_and_save_model()
        else:
            model = joblib.load(model_path)
            feature_importance = dict(zip(feature_names, model.feature_importances_))
            logger.debug("Model loaded successfully")
        
        # Create input DataFrame
        input_data = pd.DataFrame([symptoms], columns=feature_names)
        
        # Make prediction and get probability
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100  # Probability of positive class
        logger.debug(f"Prediction: {prediction}, Probability: {probability}")
        
        # Calculate result and message
        if prediction == 0:
            result = "negative"
            message = "Be happy - You are COVID Negative"
            risk_percent = min(30, probability)  # Cap negative risk at 30%
        else:
            result = "positive"
            message = "Sorry to say - You are COVID Positive"
            risk_percent = max(50, probability)  # Floor positive risk at 50%
        
        return {
            'result': result,
            'message': message,
            'risk_percent': round(risk_percent, 2),
            'feature_importance': feature_importance
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise