from django.http import JsonResponse
from .models import CustomUser


def _validate_email(request):
    """Проверка на существования анологичного email AJAX!"""
    email = request.GET.get('email', None)
    data = {
        'is_taken': CustomUser.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)
    