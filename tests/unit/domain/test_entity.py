import time
import uuid
from datetime import datetime

import pytest

from src.domain.entity import Entity

class ConcreteEntity(Entity):
    def validate(self) -> None:
        pass

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=uuid.UUID(data["id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            deleted_at=(
                datetime.fromisoformat(data["deleted_at"])
                if data["deleted_at"]
                else None
            ),
        )


@pytest.fixture
def concrete_entity():
    return ConcreteEntity()


class TestEntity:
    def test_entity_cannot_be_instantiated_directly(self):
        with pytest.raises(TypeError):
            Entity()

    def test_entity_new_instance_creation_with_no_parameters(self, concrete_entity):
        assert isinstance(concrete_entity.id, uuid.UUID)
        assert isinstance(concrete_entity.created_at, datetime)
        assert isinstance(concrete_entity.updated_at, datetime)
        assert concrete_entity.deleted_at is None
        assert concrete_entity.is_deleted is False

    def test_entity_create_with_parameters(self):
        custom_id = uuid.uuid4()
        created_at = datetime.now()
        updated_at = datetime.now()
        deleted_at = datetime.now()

        entity = ConcreteEntity(
            id=custom_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

        assert entity.id == custom_id
        assert entity.created_at == created_at
        assert entity.updated_at == updated_at
        assert entity.deleted_at == deleted_at

    def test_entity_update_updates_timestamp(self, concrete_entity):
        original_updated_at = concrete_entity.updated_at

        time.sleep(0.001)

        concrete_entity.update()

        assert concrete_entity.updated_at > original_updated_at

    def test_soft_delete(self, concrete_entity):
        concrete_entity.delete()

        assert concrete_entity.is_deleted is True
        assert isinstance(concrete_entity.deleted_at, datetime)

    def test_equality_and_hash(self):
        id1 = uuid.uuid4()
        entity1 = ConcreteEntity(id=id1)
        entity2 = ConcreteEntity(id=id1)
        entity3 = ConcreteEntity()

        assert entity1 != {}
        assert entity1 == entity2
        assert entity1 != entity3
        assert hash(entity1) == hash(entity2)

        entity_dict = {entity1: "value1"}
        assert entity_dict[entity2] == "value1"

    def test_to_dict_returns_valid_dict(self, concrete_entity):
        entity_dict = concrete_entity.to_dict()

        assert "id" in entity_dict
        assert "created_at" in entity_dict
        assert "updated_at" in entity_dict
        assert "deleted_at" in entity_dict

        assert isinstance(entity_dict["id"], str)
        assert entity_dict["id"] == str(concrete_entity.id)
        assert isinstance(entity_dict["created_at"], str)
        assert entity_dict["created_at"] == concrete_entity.created_at.isoformat()
        assert isinstance(entity_dict["updated_at"], str)
        assert entity_dict["updated_at"] == concrete_entity.updated_at.isoformat()
        if entity_dict["deleted_at"] is not None:
            assert isinstance(entity_dict["deleted_at"], str)
            assert entity_dict["deleted_at"] == concrete_entity.deleted_at.isoformat()
            
    def test_from_dict_creates_valid_instance(self, concrete_entity):
        entity_dict = concrete_entity.to_dict()
        new_entity = ConcreteEntity.from_dict(entity_dict)

        assert new_entity.id == concrete_entity.id
        assert new_entity.created_at.isoformat() == concrete_entity.created_at.isoformat()
        assert new_entity.updated_at.isoformat() == concrete_entity.updated_at.isoformat()
        if concrete_entity.deleted_at:
            assert new_entity.deleted_at.isoformat() == concrete_entity.deleted_at.isoformat()
        else:
            assert new_entity.deleted_at is None
        assert new_entity.is_deleted == concrete_entity.is_deleted

    def test_validate_does_not_raise(self):
        try:
            Entity.validate()
        except Exception as e:
            pytest.fail(f"validate() raised an exception: {e}")

    def test_to_dict_does_not_raise_exception(self, concrete_entity):
        try:
            concrete_entity.to_dict()
        except Exception as e:
            pytest.fail(f"to_dict() raised an exception: {e}")
            
    def test_from_dict_does_not_raise_exception(self, concrete_entity):
        entity_dict = concrete_entity.to_dict()
        try:
            Entity.from_dict(entity_dict)
        except Exception as e:
            pytest.fail(f"validate() raised an exception: {e}")