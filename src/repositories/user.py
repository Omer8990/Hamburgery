import logging
from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.db.connector import DbConnector
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class UserRepository:
    """
    Repository class for managing User entities in the database.

    Provides methods for retrieving, creating, updating, and deleting User records.
    """

    def __init__(self, db_connector: DbConnector):
        """
        Initializes the UserRepository with a DbConnector instance.

        :param db_connector: Instance of DbConnector for database operations.
        """
        self.db_connector = db_connector

    async def _get_user_by_id(self, user_id: int) -> User:
        """
        Private helper method to retrieve a User object by its ID.

        :param user_id: ID of the User to retrieve.
        :return: User object if found, else None.
        """
        async with self.db_connector.get_db() as db:
            query = select(User).filter(User.id == user_id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                logger.warning(f"User with ID {user_id} not found.")
            return user

    async def get_user(self, user_id: int) -> User:
        """
        Retrieves a User object by its ID.

        :param user_id: ID of the User to retrieve.
        :return: User object if found, else None.
        """
        logger.info(f"Fetching User with ID {user_id}.")
        return await self._get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a User object by its email.

        :param email: Email of the User to retrieve.
        :return: User object if found, else None.
        """
        logger.info(f"Fetching User with email {email}.")
        async with self.db_connector.get_db() as db:
            query = select(User).filter(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                logger.warning(f"User with email {email} not found.")
            return user

    async def create_user(self, user: UserCreate) -> User:
        """
        Creates a new User object in the database.

        :param user: UserCreate schema with the data for the new User.
        :return: The newly created User object.
        """
        logger.info(f"Creating new User with email {user.email}.")
        async with self.db_connector.get_db() as db:
            db_user = User(email=user.email, hashed_password=user.password)
            db.add(db_user)
            await db.refresh(db_user)
            logger.info(f"User created with ID {db_user.id}.")
            return db_user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """
        Updates an existing User object in the database.

        :param user_id: ID of the User to update.
        :param user_update: UserUpdate schema with the updated data.
        :return: The updated User object.
        :raises NotFoundException: If the User object is not found.
        """
        logger.info(f"Updating User with ID {user_id}.")

        async with self.db_connector.get_db() as db:
            query = select(User).filter(User.id == user_id)
            result = await db.execute(query)
            db_user = result.scalar_one_or_none()

            if not db_user:
                logger.error(f"Update failed: User with ID {user_id} not found.")
                raise NotFoundException(user_id)

            update_data = user_update.model_dump(exclude_unset=True)
            await db.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            await db.commit()

            updated_user = await self._get_user_by_id(user_id)
            logger.info(f"User with ID {updated_user.id} updated.")
            return updated_user

    async def delete_user(self, user_id: int) -> User:
        """
        Deletes a User object from the database by its ID.

        :param user_id: ID of the User to delete.
        :return: The deleted User object if it was found, else None.
        """
        logger.info(f"Deleting User with ID {user_id}.")
        async with self.db_connector.get_db() as db:
            db_user = await self._get_user_by_id(user_id)
            if db_user:
                await db.delete(db_user)
                logger.info(f"User with ID {user_id} deleted.")
            else:
                logger.warning(f"Delete failed: User with ID {user_id} not found.")
            return db_user
