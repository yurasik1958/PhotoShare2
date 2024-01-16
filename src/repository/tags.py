from typing import List

from sqlalchemy import select, insert, func, desc
from sqlalchemy.orm import Session

from src.database.models import Tag, tag_photo_association as t2p


class TagRepository:

    async def check_tag_exist_or_create(self, tag_name: str, session: Session) -> Tag:
        """
        Check if a tag with the specified name exists in the database.
        If the tag does not exist, create a new tag with the provided name.

        Args:
            tag_name (str): The name of the tag to check or create.
            session (Session): The database session to use for querying and creating tags.

        Returns:
            Tag: The existing or newly created Tag object.
        """
        query = select(Tag).where(Tag.name == tag_name)
        tag = session.execute(query).scalar_one_or_none()
        if tag:
            return tag
        query_ = insert(Tag).values(name=tag_name).returning(Tag)
        new_tag = session.execute(query_).scalar_one()
        session.commit()
        return new_tag


    async def add_tags_to_photo(self, tags: List[str], photo_id: int, session: Session, is_commit: bool=True) -> List[Tag]:
        """
        Add tags to a photo
        Args:
            tags_str (str): A string containing tags separated by commas.
            photo_id: The ID of the photo to which tags will be added.
            session: The database session
        Returns:
            List[Tag]: The list of tags added to the photo
        """
        result = []
        for tag in tags:
            query = select(Tag).where(Tag.name == tag)
            tag_ = session.execute(query).scalar_one_or_none()
            if not tag_:
                query_ = insert(Tag).values(name=tag).returning(Tag)
                tag_ = session.execute(query_).scalar_one()
            
            try:
                query = insert(t2p).values(tag_id=tag_.id, photo_id=photo_id).returning(t2p)
                add_tag_to_db = session.execute(query)
            except Exception as err:
                if str(err).find("duplicate key") < 0:
                    raise
                
            result.append(tag_)
        if is_commit:
            session.commit()
        return result


    async def get_tags_photo(self, photo_id: int, session: Session) -> List[Tag]:
        tquery = select(Tag).join(t2p).where(Tag.id == t2p.c.tag_id).where(t2p.c.photo_id == photo_id)
        tags = session.execute(tquery).scalars().all()
        return tags 


    async def get_different_tags(self, tags: List[str], tags_photo: List[Tag]) -> (List[str], List[str]):
        diff_list = tags
        tags_list = []
        for tag in tags_photo:
            tags_list.append(tag.name)
            try:
                idx = diff_list.index(tag.name)
                diff_list.pop(idx)
            except ValueError:
                pass
            tags_list.extend(diff_list)

        return diff_list, tags_list


    async def get_tags_all(self, session: Session) -> List[Tag]:
        # tquery = select(Tag)
        # tags = session.execute(tquery).scalars().all()
        tags = session.query(Tag) \
                      .order_by(Tag.name) \
                      .all()
        return tags 


    async def get_tags_max10(self, session: Session) -> List[Tag]:
        tags = session.query(Tag.id,
                             Tag.name,
                             func.count(Tag.id).label('tag_count')) \
                        .select_from(Tag) \
                        .join(t2p) \
                        .group_by(Tag.id, Tag.name) \
                        .order_by(desc("tag_count")) \
                        .limit(10).all()
        return tags 
