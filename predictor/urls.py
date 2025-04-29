from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction-result/', views.prediction_result, name='prediction_result'),
    #path('dashboard/', views.dash, name='dash'),
    path('account/', views.acc, name='acc'),
    path('api/predictions/', views.get_predictions, name='get_predictions'),
    path('predict/', views.predict_covid_view, name='predict_covid'),
    path('auth/logout/', views.logout_view, name='logout'),
]