import redis
import json
from services.DbManager import MongoManager
from services import LogManager
logger = LogManager.get_logger()

db_client = MongoManager()


class RedisCacheManager:
    _instance = None
    def __init__(self):
        # Initialize connection to Redis
        if RedisCacheManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                self.redis = redis.from_url("redis://127.0.0.1:6379")
                if self.redis:
                    logger.info("connected to redis client")
                RedisCacheManager._instance = self
            except redis.ConnectionError:
                logger.error("Error occurred while Connecting to redis", exc_info=True)

    @staticmethod
    def Current():
        if(RedisCacheManager._instance is None):
            RedisCacheManager._instance = RedisCacheManager()
        return RedisCacheManager._instance

    def set_value(self, encrypted_hex_card_no, json_data):
        """
        Store a list of JSON objects against an encryptedHexCardNo.

        :param encrypted_hex_card_no: The key for storing the list.
        :param json_data_list: A list of dictionaries to store as JSON strings.
        """
        # Convert list of dictionaries to a JSON string
        json_string = json.dumps(json_data)
        # Set the value in Redis
        self.redis.set(encrypted_hex_card_no, json_string)
        logger.info("Cache Set")

    def get_value(self, encrypted_hex_card_no):
        """
        Retrieve the list of JSON objects stored for a given encryptedHexCardNo.

        :param encrypted_hex_card_no: The key to retrieve the data for.
        :return: A list of dictionaries, or None if the key does not exist.
        """
        # Get the value from Redis
        result = self.redis.get(encrypted_hex_card_no)
        logger.info("Cache Get")
        if result is not None:
            # Convert JSON string back to list of dictionaries
            return json.loads(result.decode('utf-8'))

        return None

    def exists(self, encrypted_hex_card_no):
        """
        Check if there is any data stored for a specific encryptedHexCardNo.

        :param encrypted_hex_card_no: The key to check existence for.
        :return: True if the key exists, False otherwise.
        """
        return self.redis.exists(encrypted_hex_card_no) > 0

