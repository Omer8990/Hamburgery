from src.db.models.vote import Vote
from src.schemas.vote import VoteCreate, VoteUpdate
from src.exceptions import NotFoundException
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


class VoteService:
    """
    Service class for managing Vote entities.

    Provides methods for retrieving, creating, updating, and deleting Vote records.
    """

    def __init__(self, db_session: Session, vote_repository):
        """
        Initializes the VoteService with a Session instance and VoteRepository.

        :param db_session: SQLAlchemy Session instance for database operations.
        :param vote_repository: Instance of VoteRepository for database access.
        """
        self.db_session = db_session
        self.vote_repository = vote_repository

    def get_vote(self, vote_id: int) -> Vote:
        """
        Retrieves a Vote object by its ID.

        :param vote_id: ID of the Vote to retrieve.
        :return: Vote object if found, else raises NotFoundException.
        """
        logger.info(f"Fetching Vote with ID {vote_id}.")
        vote = self.vote_repository.get_vote(vote_id)
        if not vote:
            logger.warning(f"Vote with ID {vote_id} not found.")
            raise NotFoundException(vote_id)
        return vote

    def create_vote(self, vote: VoteCreate) -> Vote:
        """
        Creates a new Vote object in the database.

        :param vote: VoteCreate schema with the data for the new Vote.
        :return: The newly created Vote object.
        """
        logger.info("Creating new Vote entry.")
        db_vote = self.vote_repository.create_vote(vote)
        logger.info(f"Vote created with ID {db_vote.id}.")
        return db_vote

    def update_vote(self, vote_id: int, vote_update: VoteUpdate) -> Vote:
        """
        Updates an existing Vote object in the database.

        :param vote_id: ID of the Vote to update.
        :param vote_update: VoteUpdate schema with the updated data.
        :return: The updated Vote object.
        :raises NotFoundException: If the Vote object is not found.
        """
        logger.info(f"Updating Vote with ID {vote_id}.")
        vote = self.vote_repository.get_vote(vote_id)
        if not vote:
            logger.error(f"Update failed: Vote with ID {vote_id} not found.")
            raise NotFoundException(vote_id)

        updated_vote = self.vote_repository.update_vote(vote_id, vote_update)
        logger.info(f"Vote with ID {vote_id} updated.")
        return updated_vote

    def delete_vote(self, vote_id: int) -> Vote:
        """
        Deletes a Vote object from the database by its ID.

        :param vote_id: ID of the Vote to delete.
        :return: The deleted Vote object if it was found, else raises NotFoundException.
        """
        logger.info(f"Deleting Vote with ID {vote_id}.")
        vote = self.vote_repository.get_vote(vote_id)
        if not vote:
            logger.warning(f"Delete failed: Vote with ID {vote_id} not found.")
            raise NotFoundException(vote_id)

        deleted_vote = self.vote_repository.delete_vote(vote_id)
        logger.info(f"Vote with ID {vote_id} deleted.")
        return deleted_vote
