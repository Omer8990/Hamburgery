import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.food import FoodCreate, FoodUpdate, FoodRead
from src.db.connector import DbConnector
from src.exceptions import NotFoundException
from src.repositories.food import FoodRepository

router = APIRouter()
logger = logging.getLogger(__name__)

db_connector = DbConnector()

def get_db_session() -> Session:
    """
    Dependency that provides a SQLAlchemy session.

    Uses the DbConnector's get_db method to handle session lifecycle.
    """
    return db_connector.get_db()

def get_food_repository(db_session: Session = Depends(get_db_session)) -> FoodRepository:
    """
    Dependency that provides a FoodRepository instance.

    :param db_session: The database session for interacting with the FoodRepository.
    :return: A FoodRepository instance.
    """
    return FoodRepository(db_session)

@router.get("/foods/{food_id}", response_model=FoodRead)
def get_food(food_id: int, food_repo: FoodRepository = Depends(get_food_repository)):
    """
    Retrieve a food item by its ID.

    :param food_id: ID of the food item to retrieve.
    :param food_repo: Instance of FoodRepository to interact with the database.
    :return: The food object if found.
    :raises HTTPException: 404 error if the food item is not found.
    """
    logger.info(f"API call to fetch food with ID: {food_id}")
    food = food_repo.get_food(food_id)
    if not food:
        logger.error(f"Food with ID {food_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return food

@router.post("/foods", response_model=FoodRead, status_code=status.HTTP_201_CREATED)
def create_food(food: FoodCreate, food_repo: FoodRepository = Depends(get_food_repository)):
    """
    Create a new food item.

    :param food: FoodCreate schema with the new food data.
    :param food_repo: Instance of FoodRepository to interact with the database.
    :return: The newly created food object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new food item.")
    try:
        new_food = food_repo.create_food(food)
        logger.info(f"New food item created with ID: {new_food.id}")
        return new_food
    except SQLAlchemyError as e:
        logger.error(f"Failed to create food item: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/foods/{food_id}", response_model=FoodRead)
def update_food(food_id: int, food_update: FoodUpdate, food_repo: FoodRepository = Depends(get_food_repository)):
    """
    Update an existing food item by its ID.

    :param food_id: ID of the food item to update.
    :param food_update: FoodUpdate schema with the updated food data.
    :param food_repo: Instance of FoodRepository to interact with the database.
    :return: The updated food object.
    :raises HTTPException: 404 error if the food item is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update food item with ID: {food_id}")
    try:
        updated_food = food_repo.update_food(food_id, food_update)
        logger.info(f"Food item with ID {food_id} updated successfully")
        return updated_food
    except NotFoundException:
        logger.error(f"Food item with ID {food_id} not found for update.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    except SQLAlchemyError as e:
        logger.error(f"Failed to update food item: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/foods/{food_id}", response_model=FoodRead)
def delete_food(food_id: int, food_repo: FoodRepository = Depends(get_food_repository)):
    """
    Delete a food item by its ID.

    :param food_id: ID of the food item to delete.
    :param food_repo: Instance of FoodRepository to interact with the database.
    :return: The deleted food object.
    :raises HTTPException: 404 error if the food item is not found.
    """
    logger.info(f"API call to delete food item with ID: {food_id}")
    food = food_repo.delete_food(food_id)
    if not food:
        logger.error(f"Food item with ID {food_id} not found for deletion.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    logger.info(f"Food item with ID {food_id} deleted successfully")
    return food
