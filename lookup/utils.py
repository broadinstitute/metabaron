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

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def _intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)


def _base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return _intarr2long(struct.unpack('%sB' % len(_d), _d))

def _get_pem(key):
    exponent = _base64_to_long(key['e'])
    modulus = _base64_to_long(key['n'])
    numbers = RSAPublicNumbers(exponent, modulus)
    public_key = numbers.public_key(backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem


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
    
    tokendecode = jwt.decode(token, verify=False)
    tokenkid = jjws.get_unverified_header(token).get("kid")

    if (tokenkid and kid) and (kid==tokenkid):
        try:
            jwtson = jjwt.decode(token, key, algorithms='RS256', options={"verify_aud":False})
            return jwtson
        except Exception as e:
            print("kid in token %s" % e)

    
    if (hint and kid):
        try:
            jwtson = jjwt.decode(token, key,audience=hint,algorithms=['RS256'])
            return jwtson
        except Exception as e:
            print("hinted %s" % e)
            
    try:
        jwtson = jjwt.decode(token, key, algorithms='RS256')
        return jwtson
    except Exception as e:
        print("no hint %s" % e)

    
def checkJWKS(token):
    jwks = False
    tokendecode = None
    tokendecodeheader = None
    pubcert = None
    try:
        tokendecode = jjws.get_unverified_claims(token)
        tokendecodeheader = jjws.get_unverified_header(token)
        jwks = True
    except Exception as e:
        print(e)
        return False
    
    if not jwks:
        return False

    for uri in JWKSUri.objects.all():
        jwks_json = _getjwks(uri.URL)
        if not jwks_json:
            break
        for key in jwks_json.get('keys',None):
            #if hint in uri, use that to get cert
            #if kid in token, use that to get cert
            #otherwise try them all
            try:
                jwks = _decode_with_cert(token,key,hint=uri.hint)
                if jwks:
                    return jwks
            except Exception as e:
                print("check JWKS %s" % e)
                continue
        continue
    return False