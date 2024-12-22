from django.shortcuts import render
import logging
from django.utils import timezone

# Create your views here.

logger = logging.getLogger('documents')


# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)

def index(request):
    return render(request, 'base.html')
