from django.contrib import admin

from .models import Lookup, JWKSUri

admin.site.register(Lookup)
admin.site.register(JWKSUri)