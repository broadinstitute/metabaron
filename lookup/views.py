from django.http import HttpResponse
from .models import Lookup
from rest_framework import viewsets
from .serializers import LookupSerializer


def index(request):
    return HttpResponse("Hello, world. ")

class LookupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Lookups to be viewed or edited.
    """
    queryset = Lookup.objects.all().order_by('-short_id')
    serializer_class = LookupSerializer
