from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.vote import Vote
from src.schemas import VoteUpdate, VoteCreate
from sqlalchemy.orm import Session


class VoteRepository:
    """
    Repository class for managing Vote entities in the database.

    Provides methods for retrieving, creating, updating, and deleting Vote records.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the VoteRepository with a Session instance.

        :param db_session: SQLAlchemy Session instance for database operations.
        """
        self.db_session = db_session

    def _get_vote_by_id(self, vote_id: int) -> Vote:
        """
        Private helper method to retrieve a Vote object by its ID.

        :param vote_id: ID of the Vote to retrieve.
        :return: Vote object if found, else None.
        """
        query = select(Vote).filter(Vote.id == vote_id)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def get_vote(self, vote_id: int) -> Vote:
        """
        Retrieves a Vote object by its ID.

        :param vote_id: ID of the Vote to retrieve.
        :return: Vote object if found, else None.
        """
        return self._get_vote_by_id(vote_id)

    def create_vote(self, vote: VoteCreate) -> Vote:
        """
        Creates a new Vote object in the database.

        :param vote: VoteCreate schema with the data for the new Vote.
        :return: The newly created Vote object.
        """
        db_vote = Vote(**vote.model_dump())
        self.db_session.add(db_vote)
        self.db_session.refresh(db_vote)
        return db_vote

    def update_vote(self, vote_id: int, vote_update: VoteUpdate) -> Vote:
        """
        Updates an existing Vote object in the database.

        :param vote_id: ID of the Vote to update.
        :param vote_update: VoteUpdate schema with the updated data.
        :return: The updated Vote object.
        """
        update_data = vote_update.model_dump(exclude_unset=True)
        self.db_session.execute(
            update(Vote).where(Vote.id == vote_id).values(**update_data)
        )
        return self._get_vote_by_id(vote_id)

    def delete_vote(self, vote_id: int) -> Vote:
        """
        Deletes a Vote object from the database by its ID.

        :param vote_id: ID of the Vote to delete.
        :return: The deleted Vote object if it was found, else None.
        """
        db_vote = self._get_vote_by_id(vote_id)
        if db_vote:
            self.db_session.delete(db_vote)
        return db_vote
