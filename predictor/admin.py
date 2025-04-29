from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'risk_percent', 'prediction_time', 'patient_name')
    list_filter = ('result', 'prediction_time')
    search_fields = ('user__username', 'user__email', 'patient_name')
    ordering = ('-prediction_time',)
    readonly_fields = ('prediction_time',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset