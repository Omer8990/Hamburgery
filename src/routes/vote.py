import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from schemas.vote import VoteCreate, VoteUpdate, VoteRead
from repositories.vote import VoteRepository
from src.db.session_manager import get_db_session
from exceptions import NotFoundException

router = APIRouter()
logger = logging.getLogger(__name__)


def get_vote_repository(
    db_session: Session = Depends(get_db_session),
) -> VoteRepository:
    """
    Dependency that provides a VoteRepository instance.

    :param db_session: The database session for interacting with the VoteRepository.
    :return: A VoteRepository instance.
    """
    return VoteRepository(db_session)


@router.get("/votes/{vote_id}", response_model=VoteRead)
def get_vote(vote_id: int, vote_repo: VoteRepository = Depends(get_vote_repository)):
    """
    Retrieve a vote by its ID.

    :param vote_id: ID of the vote to retrieve.
    :param vote_repo: Instance of VoteRepository to interact with the database.
    :return: The vote object if found.
    :raises HTTPException: 404 error if the vote is not found.
    """
    logger.info(f"API call to fetch vote with ID: {vote_id}")
    vote = vote_repo.get_vote(vote_id)
    if not vote:
        logger.error(f"Vote with ID {vote_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )
    return vote


@router.post("/votes", response_model=VoteRead, status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: VoteCreate, vote_repo: VoteRepository = Depends(get_vote_repository)
):
    """
    Create a new vote.

    :param vote: VoteCreate schema with the new vote data.
    :param vote_repo: Instance of VoteRepository to interact with the database.
    :return: The newly created vote object.
    :raises HTTPException: 500 error if a database error occurs.
    """
    logger.info("API call to create a new vote")
    try:
        new_vote = vote_repo.create_vote(vote)
        logger.info(f"New vote created with ID: {new_vote.id}")
        return new_vote
    except SQLAlchemyError as e:
        logger.error(f"Failed to create vote: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.put("/votes/{vote_id}", response_model=VoteRead)
def update_vote(
    vote_id: int,
    vote_update: VoteUpdate,
    vote_repo: VoteRepository = Depends(get_vote_repository),
):
    """
    Update an existing vote by its ID.

    :param vote_id: ID of the vote to update.
    :param vote_update: VoteUpdate schema with the updated vote data.
    :param vote_repo: Instance of VoteRepository to interact with the database.
    :return: The updated vote object.
    :raises HTTPException: 404 error if the vote is not found, 500 error if a database error occurs.
    """
    logger.info(f"API call to update vote with ID: {vote_id}")
    try:
        updated_vote = vote_repo.update_vote(vote_id, vote_update)
        logger.info(f"Vote with ID {vote_id} updated successfully")
        return updated_vote
    except NotFoundException:
        logger.error(f"Vote with ID {vote_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to update vote: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete("/votes/{vote_id}", response_model=VoteRead)
def delete_vote(vote_id: int, vote_repo: VoteRepository = Depends(get_vote_repository)):
    """
    Delete a vote by its ID.

    :param vote_id: ID of the vote to delete.
    :param vote_repo: Instance of VoteRepository to interact with the database.
    :return: The deleted vote object.
    :raises HTTPException: 404 error if the vote is not found.
    """
    logger.info(f"API call to delete vote with ID: {vote_id}")
    vote = vote_repo.delete_vote(vote_id)
    if not vote:
        logger.error(f"Vote with ID {vote_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )
    logger.info(f"Vote with ID {vote_id} deleted successfully")
    return vote
