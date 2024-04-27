from rest_framework.permissions import BasePermission
from utils import AlgorandUser


class Public(BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    
class Private(BasePermission):
    
    def has_permission(self, request, view):
        return isinstance(request.user, AlgorandUser)
    
    
class WriteOnly(BasePermission):
    
    def has_permission(self, request, view):
        return True if request.method == 'POST' else isinstance(request.user, AlgorandUser)