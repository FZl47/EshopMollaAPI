from rest_framework.permissions import BasePermission
from User.models import User

class IsAuthenticated(BasePermission):
    def has_permission(self,request,view):
        data = request.data
        key = data.get('keyAPI') or None
        domain = data.get('DOMAIN') or None
        user = User.objects.filter(key=key,domain=domain).first()
        if user:
            return True
        return False