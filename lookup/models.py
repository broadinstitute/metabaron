from django.db import models
from django.core.validators import RegexValidator 
from django.db.models.fields import URLField
from base64 import b64encode,b64decode

METHODS= (
    ('GET', 'GET'),
    ('POST', 'POST')
    )

PARAMTYPE = (
    ('COOKIE','cookie'),
    ('QUERY','query string'),
    ('HEADER','HTTP Header'),
    )

#Google introspection
#url = https://www.googleapis.com/oauth2/v1/tokeninfo
#method = GET
#paramname = access_token
#extraparams = None
#paramtype = 'QUERY'
#end result = https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=<TOKEN>


class JWKSUri(models.Model):
    URL = models.URLField(max_length=200,blank=False, null=False, unique=True, help_text="JWKS URI")
    hint = models.CharField(max_length=200,blank=True,null=True,help_text="if a JWT token is expected to match some parameter in the JWKS to better match tokens to URIs")

class Lookup(models.Model):
    short_id = models.CharField(max_length=200,blank=False,null=False,unique=True,validators=[
          RegexValidator(
              regex='^[a-zA-Z0-9]*$',
              message='short_id must be Alphanumeric',
              code='invalid short_id'
          ),
      ],
        help_text="a short_id that will be used for lookups"
    )
    description = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200,blank=False,null=False,help_text="full /userinfo URL of OIDC provider")
    method = models.CharField(max_length=5,choices=METHODS,blank=False,null=False, help_text="HTTP method of access of URL")
    paramname = models.CharField(max_length=100,blank=False,null=False, default='token',help_text="What is the parameter name for the access_token to passed to URL (usually it's something like access_token)")
    paramtype = models.CharField(max_length=100,default="QUERY",choices=PARAMTYPE,blank=False,null=False,help_text="How are we passing the token to the introspector?")
    extraparams = models.CharField(max_length=200,blank=True,null=True, help_text="Extra querystring parameters in comma-separated name:value pairs")    
    basicauthid = models.CharField(max_length=200,blank=True,null=True, help_text="If userinfo uses basic auth")    
    basicauthsecret = models.CharField(max_length=200,blank=True,null=True, help_text="If userinfo uses basic auth")    

    def __str__(self):
        return self.short_id

    def constructIntrospection(self,token):
        url=None
        paramstring=None
        payload={}
        authheader=None
        if self.paramtype=="QUERY":
            payload.update({self.paramname:token})
        if self.paramtype=="HEADER":
            authheader.update({"Authorization":paramname+" "+token})
        if self.extraparams:
            params = [x.strip() for x in extraparams.split(',')]
            dict = {k:v for k,v in (x.split(':') for x in params) }
            payload.update(dict)
        if self.basicauthid and self.basicauthsecret:
            username_password = '%s:%s' % (self.basicauthid,self.basicauthsecret)
            userAndPass = b64encode(username_password.encode()).decode()
            authheader={"Authorization":"Basic "+userAndPass}
        return payload,authheader,    
