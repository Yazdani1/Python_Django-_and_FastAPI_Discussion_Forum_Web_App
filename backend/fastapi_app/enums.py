from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


ROLE_LEVELS: dict[UserRole, int] = {
    UserRole.GUEST: 0,
    UserRole.USER: 1,
    UserRole.MODERATOR: 2,
    UserRole.ADMIN: 3,
}
