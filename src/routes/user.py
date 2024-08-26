import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserUpdate, UserRead
from src.exceptions import NotFoundException
from src.services.user import UserService
from src.repositories.user import UserRepository
from src.db.session_manager import get_db_session

router = APIRouter()
logger = logging.getLogger(__name__)


def get_user_service(
    db_session: Session = Depends(get_db_session),
) -> UserService:
    """
    Dependency that provides a UserService instance.

    :param db_session: The database session for interacting with the UserService.
    :return: A UserService instance.
    """
    user_repository = UserRepository(db_session)
    return UserService(user_repository)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """
    Retrieve a user by their ID.

    :param user_id: ID of the user to retrieve.
    :param user_service: Instance of UserService to interact with the business logic.
    :return: The user object if found.
    :raises HTTPException: 404 error if the user is not found.
    """
    logger.info(f"API call to fetch user with ID: {user_id}")
    try:
        user = user_service.get_user(user_id)
        return user
    except NotFoundException:
        logger.error(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.

    :param user: UserCreate schema with the new user data.
    :param user_service: Instance of UserService to interact with the business logic.
    :return: The newly created user object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info(f"API call to create a new user with email: {user.email}")
    try:
        new_user = user_service.create_user(user)
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
    user_service: UserService = Depends(get_user_service),
):
    """
    Update an existing user by their ID.

    :param user_id: ID of the user to update.
    :param user_update: UserUpdate schema with the updated user data.
    :param user_service: Instance of UserService to interact with the business logic.
    :return: The updated user object.
    :raises HTTPException: 404 error if the user is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update user with ID: {user_id}")
    try:
        updated_user = user_service.update_user(user_id, user_update)
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
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """
    Delete a user by their ID.

    :param user_id: ID of the user to delete.
    :param user_service: Instance of UserService to interact with the business logic.
    :return: The deleted user object.
    :raises HTTPException: 404 error if the user is not found.
    """
    logger.info(f"API call to delete user with ID: {user_id}")
    try:
        user = user_service.delete_user(user_id)
        logger.info(f"User with ID {user_id} deleted successfully")
        return user
    except NotFoundException:
        logger.error(f"User with ID {user_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
