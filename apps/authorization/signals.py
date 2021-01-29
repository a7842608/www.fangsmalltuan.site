import django.dispatch

middlepeople_viewed = django.dispatch.Signal(
    providing_args=["middlepeople", "request"])
