class FoodAvailabilityNotFoundException(Exception):
    """
    Exception raised when a FoodAvailability entity is not found in the database.

    Attributes:
        food_availability_id -- the ID of the FoodAvailability that was not found
        message -- explanation of the error
    """

    def __init__(
        self, food_availability_id: int, message: str = "FoodAvailability not found"
    ):
        self.food_availability_id = food_availability_id
        self.message = f"{message}: ID {food_availability_id}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
