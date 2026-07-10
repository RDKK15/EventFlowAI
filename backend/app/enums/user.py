from enum import Enum


class UserRole(str, Enum):
    OWNER = "Owner"
    MANAGER = "Manager"
    STAFF = "Staff"