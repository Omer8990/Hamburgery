import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.day import DayCreate, DayUpdate, DayRead
from src.db.connector import DbConnector
from src.exceptions import NotFoundException
from src.repositories.day import DayRepository

router = APIRouter()
logger = logging.getLogger(__name__)

db_connector = DbConnector()

def get_db_session() -> Session:
    """
    Dependency that provides a SQLAlchemy session.

    Uses the DbConnector's get_db method to handle session lifecycle.
    """
    return db_connector.get_db()

def get_day_repository(db_session: Session = Depends(get_db_session)) -> DayRepository:
    """
    Dependency that provides a DayRepository instance.

    :param db_session: The database session for interacting with the DayRepository.
    :return: A DayRepository instance.
    """
    return DayRepository(db_session)

@router.get("/days/{day_id}", response_model=DayRead)
def get_day(day_id: int, day_repo: DayRepository = Depends(get_day_repository)):
    """
    Retrieve a Day object by its ID.

    :param day_id: ID of the Day to retrieve.
    :param day_repo: Instance of DayRepository to interact with the database.
    :return: The Day object if found.
    :raises HTTPException: 404 error if the Day object is not found.
    """
    logger.info(f"API call to fetch Day with ID: {day_id}")
    day = day_repo.get_day(day_id)
    if not day:
        logger.error(f"Day with ID {day_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    return day

@router.post("/days", response_model=DayRead, status_code=status.HTTP_201_CREATED)
def create_day(day: DayCreate, day_repo: DayRepository = Depends(get_day_repository)):
    """
    Create a new Day object.

    :param day: DayCreate schema with the new Day data.
    :param day_repo: Instance of DayRepository to interact with the database.
    :return: The newly created Day object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new Day entry.")
    try:
        new_day = day_repo.create_day(day)
        logger.info(f"New Day entry created with ID: {new_day.id}")
        return new_day
    except SQLAlchemyError as e:
        logger.error(f"Failed to create Day entry: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/days/{day_id}", response_model=DayRead)
def update_day(day_id: int, day_update: DayUpdate, day_repo: DayRepository = Depends(get_day_repository)):
    """
    Update an existing Day object by its ID.

    :param day_id: ID of the Day to update.
    :param day_update: DayUpdate schema with the updated Day data.
    :param day_repo: Instance of DayRepository to interact with the database.
    :return: The updated Day object.
    :raises HTTPException: 404 error if the Day object is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update Day with ID {day_id}")
    try:
        updated_day = day_repo.update_day(day_id, day_update)
        logger.info(f"Day with ID {day_id} updated successfully")
        return updated_day
    except NotFoundException:
        logger.error(f"Day with ID {day_id} not found for update.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    except SQLAlchemyError as e:
        logger.error(f"Failed to update Day: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/days/{day_id}", response_model=DayRead)
def delete_day(day_id: int, day_repo: DayRepository = Depends(get_day_repository)):
    """
    Delete a Day object by its ID.

    :param day_id: ID of the Day to delete.
    :param day_repo: Instance of DayRepository to interact with the database.
    :return: The deleted Day object.
    :raises HTTPException: 404 error if the Day object is not found.
    """
    logger.info(f"API call to delete Day with ID {day_id}")
    day = day_repo.delete_day(day_id)
    if not day:
        logger.error(f"Day with ID {day_id} not found for deletion.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    logger.info(f"Day with ID {day_id} deleted successfully")
    return day
