from django.http import HttpResponse
from .models import Lookup
from rest_framework import viewsets
from .serializers import LookupSerializer


def index(request):
    return HttpResponse("Hello, world. ")

class LookupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Lookups to be viewed
    Expect access token and possibly hint
    """
    queryset = Lookup.objects.all().order_by('-short_id')
    serializer_class = LookupSerializer
    lookup_field = 'short_id'
