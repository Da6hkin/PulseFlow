from rest_framework.exceptions import PermissionDenied


class SimplePermissionDenied(PermissionDenied):
    default_detail = "You are not allowed to perform this"
    default_code = 'permission_denied'
