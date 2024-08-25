class NotFoundException(Exception):
    def __init__(self, entity_id: int, entity_name: str = "Entity"):
        self.entity_id = entity_id
        self.entity_name = entity_name
        super().__init__(f"{entity_name} with ID {entity_id} not found.")

    def __str__(self):
        return f"{self.entity_name} with ID {self.entity_id} was not found."
