import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.food_availability import (
    FoodAvailabilityCreate,
    FoodAvailabilityUpdate,
    FoodAvailabilityRead,
)
from src.exceptions import NotFoundException
from src.services.food_availability import FoodAvailabilityService
from src.repositories.food_availability import FoodAvailabilityRepository
from src.db.session_manager import get_db_session

router = APIRouter()
logger = logging.getLogger(__name__)


def get_food_availability_service(
    db_session: Session = Depends(get_db_session),
) -> FoodAvailabilityService:
    """
    Dependency that provides a FoodAvailabilityService instance.

    :param db_session: The database session for interacting with the FoodAvailabilityRepository.
    :return: A FoodAvailabilityService instance.
    """
    food_availability_repository = FoodAvailabilityRepository(db_session)
    return FoodAvailabilityService(food_availability_repository)


@router.get(
    "/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead
)
def get_food_availability(
    food_availability_id: int,
    food_availability_service: FoodAvailabilityService = Depends(
        get_food_availability_service
    ),
):
    """
    Retrieve a food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to retrieve.
    :param food_availability_service: Instance of FoodAvailabilityService to interact with the service layer.
    :return: The food availability object if found.
    :raises HTTPException: 404 error if the food availability entry is not found.
    """
    logger.info(f"API call to fetch food availability with ID: {food_availability_id}")
    try:
        return food_availability_service.get_food_availability(food_availability_id)
    except NotFoundException:
        logger.error(f"Food availability with ID {food_availability_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found"
        )


@router.post(
    "/food_availabilities",
    response_model=FoodAvailabilityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_food_availability(
    food_availability: FoodAvailabilityCreate,
    food_availability_service: FoodAvailabilityService = Depends(
        get_food_availability_service
    ),
):
    """
    Create a new food availability entry.

    :param food_availability: FoodAvailabilityCreate schema with the new food availability data.
    :param food_availability_service: Instance of FoodAvailabilityService to interact with the service layer.
    :return: The newly created food availability object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new food availability entry.")
    try:
        return food_availability_service.create_food_availability(food_availability)
    except SQLAlchemyError as e:
        logger.error(f"Failed to create food availability entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.put(
    "/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead
)
def update_food_availability(
    food_availability_id: int,
    food_availability_update: FoodAvailabilityUpdate,
    food_availability_service: FoodAvailabilityService = Depends(
        get_food_availability_service
    ),
):
    """
    Update an existing food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to update.
    :param food_availability_update: FoodAvailabilityUpdate schema with the updated food availability data.
    :param food_availability_service: Instance of FoodAvailabilityService to interact with the service layer.
    :return: The updated food availability object.
    :raises HTTPException: 404 error if the food availability entry is not found, 500 error if a database error occurs.
    """
    logger.info(
        f"API call to update food availability entry with ID: {food_availability_id}"
    )
    try:
        return food_availability_service.update_food_availability(
            food_availability_id, food_availability_update
        )
    except NotFoundException:
        logger.error(
            f"Food availability entry with ID {food_availability_id} not found for update."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found"
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to update food availability entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete(
    "/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead
)
def delete_food_availability(
    food_availability_id: int,
    food_availability_service: FoodAvailabilityService = Depends(
        get_food_availability_service
    ),
):
    """
    Delete a food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to delete.
    :param food_availability_service: Instance of FoodAvailabilityService to interact with the service layer.
    :return: The deleted food availability object.
    :raises HTTPException: 404 error if the food availability entry is not found.
    """
    logger.info(
        f"API call to delete food availability entry with ID: {food_availability_id}"
    )
    try:
        return food_availability_service.delete_food_availability(food_availability_id)
    except NotFoundException:
        logger.error(
            f"Food availability entry with ID {food_availability_id} not found for deletion."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found"
        )
