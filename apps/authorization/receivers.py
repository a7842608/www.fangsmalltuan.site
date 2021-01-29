from django.dispatch import receiver
from .signals import middlepeople_viewed
from django.db.models import F


@receiver(middlepeople_viewed)
def receive_product_view(sender, middlepeople, request, **kwargs):
    middlepeople.browse_count = F('browse_count') + 1
    middlepeople.save()
