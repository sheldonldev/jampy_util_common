import uuid

import base58


def generate_short_uuid():
    # Generate a UUID1 (time-based UUID)
    raw_uuid = uuid.uuid1()

    # Convert the UUID to bytes
    uuid_bytes = raw_uuid.bytes

    # Encode the bytes to a base58 string
    base58_uuid = base58.b58encode(uuid_bytes)

    # Decode the base58 bytes to a string
    short_uuid = base58_uuid.decode('utf-8')

    return short_uuid


class UUID:
    existed_uuid_set = set()

    @staticmethod
    def get():
        return generate_short_uuid()

    @staticmethod
    def get_short(length=8):
        id = str(uuid.uuid1())[:length]
        if id not in UUID.existed_uuid_set:
            UUID.existed_uuid_set.add(id)
            return id
        else:
            return UUID.get()
