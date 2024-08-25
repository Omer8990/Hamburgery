import logging
from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.vote import Vote
from src.schemas.vote import VoteCreate, VoteUpdate
from src.db.connector import DbConnector
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class VoteRepository:
    """
    Repository class for managing Vote entities in the database.

    Provides methods for retrieving, creating, updating, and deleting Vote records.
    """

    def __init__(self, db_connector: DbConnector):
        """
        Initializes the VoteRepository with a DbConnector instance.

        :param db_connector: Instance of DbConnector for database operations.
        """
        self.db_connector = db_connector

    async def _get_vote_by_id(self, vote_id: int) -> Vote:
        """
        Private helper method to retrieve a Vote object by its ID.

        :param vote_id: ID of the Vote to retrieve.
        :return: Vote object if found, else None.
        """
        async with self.db_connector.get_db() as db:
            query = select(Vote).filter(Vote.id == vote_id)
            result = await db.execute(query)
            vote = result.scalar_one_or_none()
            if not vote:
                logger.warning(f"Vote with ID {vote_id} not found.")
            return vote

    async def get_vote(self, vote_id: int) -> Vote:
        """
        Retrieves a Vote object by its ID.

        :param vote_id: ID of the Vote to retrieve.
        :return: Vote object if found, else None.
        """
        logger.info(f"Fetching Vote with ID {vote_id}.")
        return await self._get_vote_by_id(vote_id)

    async def create_vote(self, vote: VoteCreate) -> Vote:
        """
        Creates a new Vote object in the database.

        :param vote: VoteCreate schema with the data for the new Vote.
        :return: The newly created Vote object.
        """
        logger.info("Creating new Vote entry.")
        async with self.db_connector.get_db() as db:
            db_vote = Vote(**vote.model_dump())
            db.add(db_vote)
            await db.refresh(db_vote)
            logger.info(f"Vote created with ID {db_vote.id}.")
            return db_vote

    async def update_vote(self, vote_id: int, vote_update: VoteUpdate) -> Vote:
        """
        Updates an existing Vote object in the database.

        :param vote_id: ID of the Vote to update.
        :param vote_update: VoteUpdate schema with the updated data.
        :return: The updated Vote object.
        :raises VoteNotFoundException: If the Vote object is not found.
        """
        logger.info(f"Updating Vote with ID {vote_id}.")

        async with self.db_connector.get_db() as db:
            query = select(Vote).filter(Vote.id == vote_id)
            result = await db.execute(query)
            db_vote = result.scalar_one_or_none()

            if not db_vote:
                logger.error(f"Update failed: Vote with ID {vote_id} not found.")
                raise NotFoundException(vote_id)

            update_data = vote_update.model_dump(exclude_unset=True)
            await db.execute(
                update(Vote).where(Vote.id == vote_id).values(**update_data)
            )
            await db.commit()

            updated_vote = await self._get_vote_by_id(vote_id)
            logger.info(f"Vote with ID {vote_id} updated.")
            return updated_vote

    async def delete_vote(self, vote_id: int) -> Vote:
        """
        Deletes a Vote object from the database by its ID.

        :param vote_id: ID of the Vote to delete.
        :return: The deleted Vote object if it was found, else None.
        """
        logger.info(f"Deleting Vote with ID {vote_id}.")
        async with self.db_connector.get_db() as db:
            db_vote = await self._get_vote_by_id(vote_id)
            if db_vote:
                await db.delete(db_vote)
                logger.info(f"Vote with ID {vote_id} deleted.")
            else:
                logger.warning(f"Delete failed: Vote with ID {vote_id} not found.")
            return db_vote
