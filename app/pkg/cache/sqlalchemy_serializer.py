from aiocache.serializers import BaseSerializer


class SQLAlchemySerializer(BaseSerializer):
    def dumps(self, value):
        pass

    def loads(self, value):
        pass
