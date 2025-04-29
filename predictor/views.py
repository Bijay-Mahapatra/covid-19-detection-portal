from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout
import logging
from .ml.ml_predictor import predict_covid
from .models import Prediction
from custom_auth.models import User
from django.utils import timezone
import pytz

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# View functions for rendering pages
def home(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        return render(request, 'error.html', {'message': 'Unable to load the home page'}, status=500)

def acc(request):
    try:
        return render(request, 'account.html')
    except Exception as e:
        logger.error(f"Error rendering account page: {str(e)}")
        return render(request, 'error.html', {'message': 'Unable to load the account page'}, status=500)

def medical(request):
    try:
        return render(request, 'medical-history.html')
    except Exception as e:
        logger.error(f"Error rendering medical history page: {str(e)}")
        return render(request, 'error.html', {'message': 'Unable to load the medical history page'}, status=500)

@login_required
def prediction_result(request):
    if request.method == 'POST':
        try:
            # Prepare symptoms dictionary
            symptoms = {
                'Breathing Problem': int(request.POST.get('breathing_problem', 0)),
                'Fever': int(request.POST.get('fever', 0)),
                'Dry Cough': int(request.POST.get('dry_cough', 0)),
                'Sore throat': int(request.POST.get('sore_throat', 0)),
                'Running Nose': int(request.POST.get('runny_nose', 0)),
                'Asthma': int(request.POST.get('asthma', 0)),
                'Headache': int(request.POST.get('headache', 0)),
                'Heart Disease': int(request.POST.get('heart_disease', 0)),
                'Diabetes': int(request.POST.get('diabetes', 0)),
                'Hyper Tension': int(request.POST.get('hypertension', 0)),
                'Abroad travel': int(request.POST.get('abroad_travel', 0)),
                'Contact with COVID Patient': int(request.POST.get('contact_covid', 0)),
                'Attended Large Gathering': int(request.POST.get('attended_gathering', 0)),
                'Visited Public Exposed Places': int(request.POST.get('visited_public_areas', 0)),
                'Family working in Public Exposed Places': int(request.POST.get('family_working_in_public', 0))
            }
            
            # Get model prediction
            prediction_result = predict_covid(symptoms)
            
            # Prepare selected symptoms for display
            selected_symptoms = [key for key, value in symptoms.items() if value == 1]
            
            patient_name = request.POST.get('patientName', request.user.get_full_name())
            Prediction.objects.create(
                user=request.user,
                result=prediction_result['result'].lower(),
                risk_percent=prediction_result['risk_percent'],
                symptoms=selected_symptoms,
                patient_name=patient_name
            )
            
            context = {
                'result': prediction_result['result'],
                'message': prediction_result['message'],
                'risk_percent': prediction_result['risk_percent'],
                'selected_symptoms': selected_symptoms,
                'patient_info': {
                    'name': patient_name,
                    'age': request.POST.get('patientAge', ''),
                    'gender': request.POST.get('patientGender', ''),
                    'notes': request.POST.get('patientNotes', '')
                },
                'feature_importance': prediction_result['feature_importance']
            }
            return render(request, 'prediction_result.html', context)
        except Exception as e:
            logger.error(f"Error processing prediction result: {str(e)}")
            return render(request, 'error.html', {'message': 'Unable to process prediction'}, status=500)
    
    return redirect('home')

@login_required
def predict_covid_view(request):
    if request.method == 'POST':
        try:
            # Prepare symptoms dictionary
            symptoms = {
                'Breathing Problem': int(request.POST.get('breathing_problem', 0)),
                'Fever': int(request.POST.get('fever', 0)),
                'Dry Cough': int(request.POST.get('dry_cough', 0)),
                'Sore throat': int(request.POST.get('sore_throat', 0)),
                'Running Nose': int(request.POST.get('runny_nose', 0)),
                'Asthma': int(request.POST.get('asthma', 0)),
                'Headache': int(request.POST.get('headache', 0)),
                'Heart Disease': int(request.POST.get('heart_disease', 0)),
                'Diabetes': int(request.POST.get('diabetes', 0)),
                'Hyper Tension': int(request.POST.get('hypertension', 0)),
                'Abroad travel': int(request.POST.get('abroad_travel', 0)),
                'Contact with COVID Patient': int(request.POST.get('contact_covid', 0)),
                'Attended Large Gathering': int(request.POST.get('attended_gathering', 0)),
                'Visited Public Exposed Places': int(request.POST.get('visited_public_areas', 0)),
                'Family working in Public Exposed Places': int(request.POST.get('family_working_in_public', 0))
            }
            logger.debug(f"Received symptoms: {symptoms}")
            
            # Get prediction
            prediction_result = predict_covid(symptoms)
            
            # Get patient info
            patient_info = {
                'name': request.POST.get('patientName', request.user.get_full_name()),
                'age': request.POST.get('patientAge', ''),
                'gender': request.POST.get('patientGender', ''),
                'notes': request.POST.get('patientNotes', '')
            }
            
            return JsonResponse({
                'status': 'success',
                'result': prediction_result['result'],
                'message': prediction_result['message'],
                'risk_percent': prediction_result['risk_percent'],
                'patient_info': patient_info,
                'feature_importance': prediction_result['feature_importance']
            })
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Prediction failed: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required
def get_predictions(request):
    try:
        predictions = Prediction.objects.filter(user=request.user).order_by('-prediction_time')
        logger.debug(f"Found {predictions.count()} predictions for user {request.user.username}")
        predictions_data = [
            {
                'id': pred.id,
                'predictionTime': timezone.localtime(pred.prediction_time, timezone=pytz.timezone('Asia/Kolkata')).strftime('%d/%m/%Y, %I:%M:%S %p'),
                'result': pred.result,
                'confidence': pred.risk_percent,
                'symptoms': pred.symptoms,
                'patientName': pred.patient_name
            } for pred in predictions
        ]
        logger.debug(f"Sending predictions: {predictions_data}")
        return JsonResponse({
            'status': 'success',
            'predictions': predictions_data
        })
    except Exception as e:
        logger.error(f"Error fetching predictions: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@ensure_csrf_cookie
def logout_view(request):
    try:
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)  # This clears the user's session
            logger.info(f"User {username} logged out successfully")
            return JsonResponse({
                'success': True,
                'message': 'Successfully logged out'
            }, status=200)
        else:
            logger.info("Logout attempted by unauthenticated user")
            return JsonResponse({
                'success': False,
                'message': 'Already logged out'
            }, status=200)
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f"Logout failed: {str(e)}"
        }, status=500)