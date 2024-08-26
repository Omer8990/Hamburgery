from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.db.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """
    Repository class for managing User entities in the database.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the UserRepository with a Session instance.

        :param db_session: SQLAlchemy Session instance for database operations.
        """
        self.db_session = db_session

    def get_user(self, user_id: int) -> User:
        """
        Retrieves a User object by its ID.

        :param user_id: ID of the User to retrieve.
        :return: User object if found, else None.
        """
        query = select(User).filter(User.id == user_id)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a User object by its email.

        :param email: Email of the User to retrieve.
        :return: User object if found, else None.
        """
        query = select(User).filter(User.email == email)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def create_user(self, user: UserCreate) -> User:
        """
        Creates a new User object in the database.

        :param user: UserCreate schema with the data for the new User.
        :return: The newly created User object.
        """
        db_user = User(email=user.email, hashed_password=user.password)
        self.db_session.add(db_user)
        self.db_session.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """
        Updates an existing User object in the database.

        :param user_id: ID of the User to update.
        :param user_update: UserUpdate schema with the updated data.
        :return: The updated User object.
        """
        update_data = user_update.model_dump(exclude_unset=True)
        self.db_session.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        query = select(User).filter(User.id == user_id)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def delete_user(self, user_id: int) -> User:
        """
        Deletes a User object from the database by its ID.

        :param user_id: ID of the User to delete.
        :return: The deleted User object if it was found, else None.
        """
        query = select(User).filter(User.id == user_id)
        result = self.db_session.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user:
            self.db_session.delete(db_user)
        return db_user
