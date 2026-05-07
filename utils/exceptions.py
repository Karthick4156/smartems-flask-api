class BadRequestException(Exception):
    def __init__(self, message="Bad request"):
        self.message = message


class NotFoundException(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message


class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message="Forbidden"):
        self.message = message