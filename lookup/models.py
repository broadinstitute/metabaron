from django.db import models
from django.core.validators import RegexValidator 

METHODS= (
    ('GET', 'GET'),
    ('POST', 'POST')
    )

PARAMTYPE = (
    ('COOKIE','cookie'),
    ('QUERY','query string'),
    ('HEADER','HTTP Header'),
    )

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
    paramtype = models.CharField(max_length=10,choices=PARAMTYPE,blank=False,null=False, help_text="How is access_token passed to URL")
    paramname = models.CharField(max_length=100,blank=False,null=False, help_text="What is the parameter name for the access_token to passed to URL (usually it's something like access_token)")
