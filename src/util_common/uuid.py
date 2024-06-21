from uuid import uuid1


class UUID:
    existed_uuid_set = set()

    @staticmethod
    def get(length=8):
        uuid = str(uuid1())[:length]
        if uuid not in UUID.existed_uuid_set:
            UUID.existed_uuid_set.add(uuid)
            return uuid
        else:
            return UUID.get()
