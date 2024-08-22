class DayNotFoundException(Exception):
    """
    Exception raised when a Day entity is not found in the database.

    Attributes:
        day_id -- the ID of the Day that was not found
        message -- explanation of the error
    """

    def __init__(self, day_id: int, message: str = "Day not found"):
        self.day_id = day_id
        self.message = f"{message}: ID {day_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
