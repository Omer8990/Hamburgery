class FoodNotFoundException(Exception):
    """
    Exception raised when a Food entity is not found in the database.

    Attributes:
        food_id -- the ID of the Food that was not found
        message -- explanation of the error
    """

    def __init__(self, food_id: int, message: str = "Food not found"):
        self.food_id = food_id
        self.message = f"{message}: ID {food_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
