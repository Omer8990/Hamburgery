import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from src.schemas.food import FoodCreate, FoodUpdate, FoodRead
from src.db.session_manager import get_db_session
from src.services.food import FoodService
from src.exceptions import NotFoundException
from src.services.food import FoodService
from src.repositories.food import FoodRepository

router = APIRouter()
logger = logging.getLogger(__name__)


def get_food_service(
    db_session: Session = Depends(get_db_session),
) -> FoodService:
    """
    Dependency that provides a FoodService instance.

    :param db_session: The database session for interacting with the FoodRepository.
    :return: A FoodService instance.
    """
    food_repository = FoodRepository(db_session)
    return FoodService(food_repository)


@router.get("/foods/{food_id}", response_model=FoodRead)
def get_food(food_id: int, food_service: FoodService = Depends(get_food_service)):
    """
    Retrieve a food item by its ID.

    :param food_id: ID of the food item to retrieve.
    :param food_service: Instance of FoodService to interact with the database.
    :return: The food object if found.
    :raises HTTPException: 404 error if the food item is not found.
    """
    logger.info(f"API call to fetch food with ID: {food_id}")
    try:
        return food_service.get_food(food_id)
    except NotFoundException:
        logger.error(f"Food with ID {food_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )


@router.post("/foods", response_model=FoodRead, status_code=status.HTTP_201_CREATED)
def create_food(
    food: FoodCreate, food_service: FoodService = Depends(get_food_service)
):
    """
    Create a new food item.

    :param food: FoodCreate schema with the new food data.
    :param food_service: Instance of FoodService to interact with the database.
    :return: The newly created food object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new food item.")
    try:
        return food_service.create_food(food)
    except SQLAlchemyError as e:
        logger.error(f"Failed to create food item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.put("/foods/{food_id}", response_model=FoodRead)
def update_food(
    food_id: int,
    food_update: FoodUpdate,
    food_service: FoodService = Depends(get_food_service),
):
    """
    Update an existing food item by its ID.

    :param food_id: ID of the food item to update.
    :param food_update: FoodUpdate schema with the updated food data.
    :param food_service: Instance of FoodService to interact with the database.
    :return: The updated food object.
    :raises HTTPException: 404 error if the food item is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update food item with ID: {food_id}")
    try:
        return food_service.update_food(food_id, food_update)
    except NotFoundException:
        logger.error(f"Food item with ID {food_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to update food item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete("/foods/{food_id}", response_model=FoodRead)
def delete_food(food_id: int, food_service: FoodService = Depends(get_food_service)):
    """
    Delete a food item by its ID.

    :param food_id: ID of the food item to delete.
    :param food_service: Instance of FoodService to interact with the database.
    :return: The deleted food object.
    :raises HTTPException: 404 error if the food item is not found.
    """
    logger.info(f"API call to delete food item with ID: {food_id}")
    try:
        return food_service.delete_food(food_id)
    except NotFoundException:
        logger.error(f"Food item with ID {food_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )
