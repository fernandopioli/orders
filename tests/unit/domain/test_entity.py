import time
import uuid
from datetime import datetime

import pytest

from src.domain.entity import Entity


class ConcreteEntity(Entity):
        def validate(self) -> None:
                pass
        
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

        assert entity1 == entity2
        assert entity1 != entity3
        assert hash(entity1) == hash(entity2)

        entity_dict = {entity1: "value1"}
        assert entity_dict[entity2] == "value1"
