from django.utils import timezone


def year(request):
    """Adds a variable with the current year."""
    return {
        'year': timezone.now().year
    }
