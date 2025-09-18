from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import Token 
def enforce_csrf(request):
    check = CSRFCheck(lambda req:None)
    check.process_request(request)
    reason = check.process_view(request,None,(),{})
    if reason:
        raise exceptions.PermissionDenied(f"CSRF Failed::{reason}")

class CustomAuthentication(JWTAuthentication):
    def authenticate(self,request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        if access_token is None:
            return None 
        validated_token = self.get_validated_token(raw_token=access_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token