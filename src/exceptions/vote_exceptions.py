class VoteNotFoundException(Exception):
    """
    Exception raised when a Vote entity is not found in the database.

    Attributes:
        vote_id -- the ID of the Vote that was not found
        message -- explanation of the error
    """

    def __init__(self, vote_id: int, message: str = "Vote not found"):
        self.vote_id = vote_id
        self.message = f"{message}: ID {vote_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
