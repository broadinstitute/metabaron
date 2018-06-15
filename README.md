# metabaron
OIDC access_token userinfo endpoint for multiple Providers. Introspects both opaque and JWT tokens. Used as a /userinfo endpoint in your favorite resource server. Useful if you want to "trust" multiple Oauth Providers.

format for sending to metabaron:
`https://metabaron/introspect/?access_token=<token>` or `Authorization: Bearer <token> https://metabaron/introspect/`

# startup
`DJANGO_SETTINGS_MODULE=metabaron.settings.local sh scripts/start.sh` -- alter the `metabaron/settings/<file>` if you want different settings on startup. For instance if you want to point at a real DB.  

Alter `metabaron/scripts/start.sh` if you want a different username/password as your admin. You can change after startup, too.  

# first login
go to `http://localhost:8000/admin/` or however you set it up and use your username/password. Add JWKS URLs if they exist and add Introspection endpoints. Google and Globus are there by default. Globus Introspection will need clientID and Secret to auth to their endpoint.

# docker and docker-compose
```
docker-compose -f docker-compose.yaml -p metabaron build
docker-compose -f docker-compose.yaml -p metabaron up
```
You might want to alter `metabaron/settings/dockercompose.py` to fit you. You might want to alter `scripts/nginx.conf`. This is where you'd do ssl via nginx (recommended). 
