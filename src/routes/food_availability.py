import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.food_availability import FoodAvailabilityCreate, FoodAvailabilityUpdate, FoodAvailabilityRead
from src.db.connector import DbConnector
from src.exceptions import NotFoundException
from src.repositories.food_availability import FoodAvailabilityRepository

router = APIRouter()
logger = logging.getLogger(__name__)

db_connector = DbConnector()

def get_db_session() -> Session:
    """
    Dependency that provides a SQLAlchemy session.

    Uses the DbConnector's get_db method to handle session lifecycle.
    """
    return db_connector.get_db()

def get_food_availability_repository(db_session: Session = Depends(get_db_session)) -> FoodAvailabilityRepository:
    """
    Dependency that provides a FoodAvailabilityRepository instance.

    :param db_session: The database session for interacting with the FoodAvailabilityRepository.
    :return: A FoodAvailabilityRepository instance.
    """
    return FoodAvailabilityRepository(db_session)

@router.get("/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead)
def get_food_availability(food_availability_id: int, food_availability_repo: FoodAvailabilityRepository = Depends(get_food_availability_repository)):
    """
    Retrieve a food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to retrieve.
    :param food_availability_repo: Instance of FoodAvailabilityRepository to interact with the database.
    :return: The food availability object if found.
    :raises HTTPException: 404 error if the food availability entry is not found.
    """
    logger.info(f"API call to fetch food availability with ID: {food_availability_id}")
    food_availability = food_availability_repo.get_food_availability(food_availability_id)
    if not food_availability:
        logger.error(f"Food availability with ID {food_availability_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found")
    return food_availability

@router.post("/food_availabilities", response_model=FoodAvailabilityRead, status_code=status.HTTP_201_CREATED)
def create_food_availability(food_availability: FoodAvailabilityCreate, food_availability_repo: FoodAvailabilityRepository = Depends(get_food_availability_repository)):
    """
    Create a new food availability entry.

    :param food_availability: FoodAvailabilityCreate schema with the new food availability data.
    :param food_availability_repo: Instance of FoodAvailabilityRepository to interact with the database.
    :return: The newly created food availability object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new food availability entry.")
    try:
        new_food_availability = food_availability_repo.create_food_availability(food_availability)
        logger.info(f"New food availability entry created with ID: {new_food_availability.id}")
        return new_food_availability
    except SQLAlchemyError as e:
        logger.error(f"Failed to create food availability entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead)
def update_food_availability(food_availability_id: int, food_availability_update: FoodAvailabilityUpdate, food_availability_repo: FoodAvailabilityRepository = Depends(get_food_availability_repository)):
    """
    Update an existing food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to update.
    :param food_availability_update: FoodAvailabilityUpdate schema with the updated food availability data.
    :param food_availability_repo: Instance of FoodAvailabilityRepository to interact with the database.
    :return: The updated food availability object.
    :raises HTTPException: 404 error if the food availability entry is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update food availability entry with ID: {food_availability_id}")
    try:
        updated_food_availability = food_availability_repo.update_food_availability(food_availability_id, food_availability_update)
        logger.info(f"Food availability entry with ID {food_availability_id} updated successfully")
        return updated_food_availability
    except NotFoundException:
        logger.error(f"Food availability entry with ID {food_availability_id} not found for update.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found")
    except SQLAlchemyError as e:
        logger.error(f"Failed to update food availability entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/food_availabilities/{food_availability_id}", response_model=FoodAvailabilityRead)
def delete_food_availability(food_availability_id: int, food_availability_repo: FoodAvailabilityRepository = Depends(get_food_availability_repository)):
    """
    Delete a food availability entry by its ID.

    :param food_availability_id: ID of the food availability entry to delete.
    :param food_availability_repo: Instance of FoodAvailabilityRepository to interact with the database.
    :return: The deleted food availability object.
    :raises HTTPException: 404 error if the food availability entry is not found.
    """
    logger.info(f"API call to delete food availability entry with ID: {food_availability_id}")
    food_availability = food_availability_repo.delete_food_availability(food_availability_id)
    if not food_availability:
        logger.error(f"Food availability entry with ID {food_availability_id} not found for deletion.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food availability not found")
    logger.info(f"Food availability entry with ID {food_availability_id} deleted successfully")
    return food_availability
