from .models import Lookup,JWKSUri
import requests
import re
import jwt
from jose import jws as jjws
from jose import jwk as jjwk
from jose import jwt as jjwt
import json
import base64

import six
import struct

def get_token(request):
    token=None
    try:
        if request.META.get('HTTP_AUTHORIZATION'):
            fulltoken = request.META.get('HTTP_AUTHORIZATION',None)
            return fulltoken[7:len(fulltoken)]
    except:
        pass
    token = request.query_params.get("access_token", None)
    return token

def _getjwks(uri):
    try:
        response = requests.get(uri)
        return response.json()
    except:
        pass
    return None

def _decode_with_cert(token,key,hint=None):
    kid = key.get('kid',None)
    tokenkid = None
    pubcert = None
    jwtson = None
    
    tokendecode = jjws.get_unverified_claims(token)
    tokenkid = jjws.get_unverified_header(token).get("kid")

    if (tokenkid and kid) and (kid==tokenkid):
        try:
            jwtson = jjwt.decode(token, key, algorithms='RS256', options={'verify_aud': False})
            return jwtson
        except Exception as e:
            print("kid in token: Cannot be introspected in JWKS %s" % e)
    
def checkJWKS(token):
    jwks = False
    tokendecode = None
    tokendecodeheader = None
    pubcert = None
    message = None
    #not a JWT at all -- not an error condition, just a reality.
    try:
        tokendecode = jjws.get_unverified_claims(token)
        tokendecodeheader = jjws.get_unverified_header(token)
        jwks = True
    except Exception as e:
        print(e)
        return False
    
    for uri in JWKSUri.objects.all():
        jwks_json = _getjwks(uri.URL)
        if not jwks_json:
            break
        for key in jwks_json.get('keys',None):
            try:
                jwks = _decode_with_cert(token,key,hint=uri.hint)
                if jwks:
                    return jwks
            except Exception as e:
                print("check JWKS %s" % e)
                continue
        continue
    return False

def _introspect(endpoint,payload,header):
    r = None
    if endpoint.method=="GET":
        r = requests.get(
            endpoint.url,
            params=payload,
            headers=header
            )
    if endpoint.method=="POST":
        header.update({"Content-Type": "application/x-www-form-urlencoded"})        
        r = requests.post(
            endpoint.url,
            data=payload,
            headers=header
            )

    print(header)
    print(payload)

    if not r:
        return None
    return r.json()

def checkOpaque(token):
    opaque=False
    for endpoint in Lookup.objects.all():
        payload,header = endpoint.constructIntrospection(token)

        try:
            opaque = _introspect(endpoint,payload,header)
            if opaque:
                return opaque 
        except Exception as e:
            print("Opaque failed %s:" % e)
            continue
    return False