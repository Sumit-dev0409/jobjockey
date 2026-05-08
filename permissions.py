def has_permission(user, perm: str) -> bool:
    if user.role == "admin":
        return True
    if not user.permissions:
        return False
    return perm in user.permissions