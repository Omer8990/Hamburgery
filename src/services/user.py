import logging
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.db.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.exceptions import NotFoundException
from src.repositories.user import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for managing User entities.

    Handles business logic for retrieving, creating, updating, and deleting User records.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the UserService with a UserRepository instance.

        :param user_repository: Instance of UserRepository for database operations.
        """
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:
        """
        Retrieves a User object by its ID.

        :param user_id: ID of the User to retrieve.
        :return: User object if found, else raises NotFoundException.
        """
        logger.info(f"Fetching User with ID {user_id}.")
        user = self.user_repository.get_user(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found.")
            raise NotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a User object by its email.

        :param email: Email of the User to retrieve.
        :return: User object if found, else raises NotFoundException.
        """
        logger.info(f"Fetching User with email {email}.")
        user = self.user_repository.get_user_by_email(email)
        if not user:
            logger.error(f"User with email {email} not found.")
            raise NotFoundException(f"User with email {email} not found.")
        return user

    def create_user(self, user: UserCreate) -> User:
        """
        Creates a new User object.

        :param user: UserCreate schema with the data for the new User.
        :return: The newly created User object.
        """
        logger.info(f"Creating new User with email {user.email}.")
        new_user = self.user_repository.create_user(user)
        logger.info(f"User created with ID {new_user.id}.")
        return new_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """
        Updates an existing User object.

        :param user_id: ID of the User to update.
        :param user_update: UserUpdate schema with the updated data.
        :return: The updated User object.
        :raises NotFoundException: If the User object is not found.
        """
        logger.info(f"Updating User with ID {user_id}.")
        user = self.user_repository.get_user(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found.")
            raise NotFoundException(f"User with ID {user_id} not found.")

        updated_user = self.user_repository.update_user(user_id, user_update)
        logger.info(f"User with ID {updated_user.id} updated.")
        return updated_user

    def delete_user(self, user_id: int) -> User:
        """
        Deletes a User object.

        :param user_id: ID of the User to delete.
        :return: The deleted User object.
        :raises NotFoundException: If the User object is not found.
        """
        logger.info(f"Deleting User with ID {user_id}.")
        user = self.user_repository.get_user(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found.")
            raise NotFoundException(f"User with ID {user_id} not found.")

        deleted_user = self.user_repository.delete_user(user_id)
        logger.info(f"User with ID {user_id} deleted.")
        return deleted_user
