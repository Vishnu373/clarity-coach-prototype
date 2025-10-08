import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_CONNECTION_STRING, MONGODB_DATABASE_NAME

logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self):
        self.client = None
        self.database = None
        self._connect()
    
    def _connect(self):
        try:
            if not MONGODB_CONNECTION_STRING:
                raise ValueError("MONGODB_CONNECTION_STRING not found in environment variables")
            
            self.client = MongoClient(MONGODB_CONNECTION_STRING, server_api=ServerApi('1'))
            self.database = self.client[MONGODB_DATABASE_NAME]
            
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    
    def get_collection(self, collection_name):
        return self.database[collection_name]

mongodb_client = MongoDBClient()
