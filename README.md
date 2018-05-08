# metabaron
OIDC access_token userinfo endpoint for multiple Providers

format for sending to metabaron:
`https://metabaron/introspect?access_token=<token>` or `Authorization: Bearer <token> https://metabaron/introspect`

# startup
`DJANGO_SETTINGS_MODULE=metabaron.settings.local sh scripts/start.sh`