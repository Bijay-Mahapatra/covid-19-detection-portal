from django.db import models
from custom_auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    result = models.CharField(max_length=10, choices=[('positive', 'Positive'), ('negative', 'Negative')])
    risk_percent = models.FloatField()
    symptoms = models.JSONField()  # Store symptoms as a JSON list
    prediction_time = models.DateTimeField(auto_now_add=True)
    patient_name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-prediction_time']  # Latest predictions first

    def __str__(self):
        return f"{self.user.username} - {self.result} - {self.prediction_time}"