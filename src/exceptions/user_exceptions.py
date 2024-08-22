class UserNotFoundException(Exception):
    """
    Exception raised when a User entity is not found in the database.

    Attributes:
        user_id -- the ID of the User that was not found
        message -- explanation of the error
    """

    def __init__(self, user_id: int, message: str = "User not found"):
        self.user_id = user_id
        self.message = f"{message}: ID {user_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
