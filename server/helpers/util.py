"""
Utility Functions
"""
import json
from datetime import datetime


def serialize_to_json(data):
    """ Serialize an object to JSON, ensuring that the datetimes are formatted
    according to RFC 3339

    Args:
        obj: the object to serialize to JSON
    """

    # Define the actual datetime serializer
    # See: https://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python#8556555
    def datetime_serializer(element):
        if isinstance(element, datetime):
            return element.isoformat("T") + "Z"

    return json.dumps(data, default=datetime_serializer)
