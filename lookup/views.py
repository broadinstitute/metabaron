from django.http import HttpResponse
from .models import Lookup
from rest_framework import viewsets
from .serializers import LookupSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .utils import get_token,checkJWKS

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


#non hinted
#cycle through all
#first check JWKS URI if decode-able, lookup kid
#if opaque try hinted logic based on referrer
# if basic/secret exist, make sure to auth with url
# expect token in query string param and passed on to url with params
# process through "rules engine to determine where the token came from"  and introspect
# return 400 invalid if nothing, return 200 with data if something.  

class IntrospectList(generics.ListCreateAPIView):
    queryset = Lookup.objects.all().order_by('-short_id')
    serializer_class = LookupSerializer

    def list(self, request, format=None):
        queryset = self.get_queryset()
        token=get_token(request)
        if not token:
            return Response(data={"error":"NO Token"},status=500)
        
        #if jwt try JWKS first
        jwks = checkJWKS(token)
        if jwks:
            return Response(jwks,status=200)
        
        return Response(data={"error":"Token cannot be introspected"},status=401)