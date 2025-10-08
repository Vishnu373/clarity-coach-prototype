import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from utils.mongodb_client import mongodb_client
from config import MONGODB_COLLECTION_NAME
from bson import ObjectId

logger = logging.getLogger(__name__)

def save_resume(resume_data: Dict[str, Any], filename: str, file_size: int, user_id: str = None) -> str:

    try:
        collection = mongodb_client.get_collection(MONGODB_COLLECTION_NAME)
        
        document = {
            **resume_data,
            "metadata": {
                "filename": filename,
                "file_size": file_size,
                "uploaded_at": datetime.utcnow(),
                "processing_version": "v2.0"
            }
        }
        
        # Add user_id if provided (for future Clerk integration)
        if user_id:
            document["clerk_user_id"] = user_id
        
        # Insert document
        result = collection.insert_one(document)
        
        logger.info(f"Resume saved successfully with ID: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        logger.error(f"Failed to save resume: {e}")
        raise Exception(f"Database save failed: {str(e)}")

def get_resume(resume_id: str) -> Optional[Dict[str, Any]]:
    try:
        collection = mongodb_client.get_collection(MONGODB_COLLECTION_NAME)
        
        resume = collection.find_one({"_id": ObjectId(resume_id)})
        
        if resume:
            resume["_id"] = str(resume["_id"])
            logger.info(f"Resume retrieved successfully: {resume_id}")
            return resume

        else:
            logger.warning(f"Resume not found: {resume_id}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to get resume {resume_id}: {e}")
        return None

def get_user_resumes(user_id: str) -> List[Dict[str, Any]]:
    try:
        collection = mongodb_client.get_collection(MONGODB_COLLECTION_NAME)
        
        resumes = list(collection.find({"clerk_user_id": user_id}))
        
        # Convert ObjectIds to strings
        for resume in resumes:
            resume["_id"] = str(resume["_id"])
        
        logger.info(f"Retrieved {len(resumes)} resumes for user {user_id}")
        return resumes
        
    except Exception as e:
        logger.error(f"Failed to get user resumes for {user_id}: {e}")
        return []