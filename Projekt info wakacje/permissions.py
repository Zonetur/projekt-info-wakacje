def has_permission(user, perm):
    return user and (user.role == "admin" or perm in user.permissions)
