import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserUpdate, UserRead
from src.exceptions import NotFoundException
from src.repositories.user import UserRepository
from src.db.session_manager import get_db_session


router = APIRouter()
logger = logging.getLogger(__name__)


def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.

    :param db_session: The database session for interacting with the UserRepository.
    :return: A UserRepository instance.
    """
    return UserRepository(db_session)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    """
    Retrieve a user by their ID.

    :param user_id: ID of the user to retrieve.
    :param user_repo: Instance of UserRepository to interact with the database.
    :return: The user object if found.
    :raises HTTPException: 404 error if the user is not found.
    """
    logger.info(f"API call to fetch user with ID: {user_id}")
    user = user_repo.get_user(user_id)
    if not user:
        logger.error(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Create a new user.

    :param user: UserCreate schema with the new user data.
    :param user_repo: Instance of UserRepository to interact with the database.
    :return: The newly created user object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info(f"API call to create a new user with email: {user.email}")
    try:
        new_user = user_repo.create_user(user)
        logger.info(f"New user created with ID: {new_user.id}")
        return new_user
    except SQLAlchemyError as e:
        logger.error(f"Failed to create user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_repo: UserRepository = Depends(get_user_repository),
):
    """
    Update an existing user by their ID.

    :param user_id: ID of the user to update.
    :param user_update: UserUpdate schema with the updated user data.
    :param user_repo: Instance of UserRepository to interact with the database.
    :return: The updated user object.
    :raises HTTPException: 404 error if the user is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update user with ID: {user_id}")
    try:
        updated_user = user_repo.update_user(user_id, user_update)
        logger.info(f"User with ID {user_id} updated successfully")
        return updated_user
    except NotFoundException:
        logger.error(f"User with ID {user_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to update user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    """
    Delete a user by their ID.

    :param user_id: ID of the user to delete.
    :param user_repo: Instance of UserRepository to interact with the database.
    :return: The deleted user object.
    :raises HTTPException: 404 error if the user is not found.
    """
    logger.info(f"API call to delete user with ID: {user_id}")
    user = user_repo.delete_user(user_id)
    if not user:
        logger.error(f"User with ID {user_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(f"User with ID {user_id} deleted successfully")
    return user
