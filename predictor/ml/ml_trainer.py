from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings
import logging
from .ml_utils import load_and_preprocess_data

logger = logging.getLogger(__name__)

def train_and_save_model():
    """
    Train a RandomForestClassifier model and save it.
    Returns: Trained model and feature importance dictionary
    """
    try:
        # Load and preprocess data
        df = load_and_preprocess_data()
        X = df.drop(columns=['COVID-19'])
        y = df['COVID-19']
        
        # Train RandomForestClassifier
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=5,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        model.fit(X, y)
        
        # Save the model
        model_path = os.path.join(settings.BASE_DIR, 'covid_model.joblib')
        joblib.dump(model, model_path)
        logger.info(f"Model trained and saved to: {model_path}")
        
        # Get feature importance
        feature_importance = dict(zip(X.columns, model.feature_importances_))
        logger.debug(f"Feature importance: {feature_importance}")
        
        return model, feature_importance
    
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise