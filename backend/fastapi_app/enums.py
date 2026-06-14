from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class VoteType(str, PyEnum):
    UP = "up"
    DOWN = "down"


class ModerationAction(str, PyEnum):
    BLOCK_USER = "block_user"
    UNBLOCK_USER = "unblock_user"


ROLE_LEVELS: dict[UserRole, int] = {
    UserRole.GUEST: 0,
    UserRole.USER: 1,
    UserRole.MODERATOR: 2,
    UserRole.ADMIN: 3,
}
