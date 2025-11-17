import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
import aiofiles

class DocumentStorage:
    def __init__(self, base_path: str = "uploads"):
        self.base_path = base_path
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.base_path,
            f"{self.base_path}/resumes",
            f"{self.base_path}/photos", 
            f"{self.base_path}/certificates",
            f"{self.base_path}/compliance"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def save_document(self, file: UploadFile, user_id: str, doc_type: str) -> dict:
        """Save uploaded document with proper organization"""
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
        
        # Determine storage path based on document type
        if doc_type == "resume":
            storage_path = f"{self.base_path}/resumes/{unique_filename}"
        elif doc_type == "photo":
            storage_path = f"{self.base_path}/photos/{unique_filename}"
        elif doc_type == "certificate":
            storage_path = f"{self.base_path}/certificates/{unique_filename}"
        else:
            storage_path = f"{self.base_path}/{unique_filename}"
        
        # Save file
        async with aiofiles.open(storage_path, 'wb') as buffer:
            content = await file.read()
            await buffer.write(content)
        
        return {
            "filename": unique_filename,
            "original_name": file.filename,
            "file_path": storage_path,
            "file_size": len(content),
            "file_type": file.content_type,
            "document_type": doc_type,
            "uploaded_at": datetime.now().isoformat()
        }
    
    async def get_document_path(self, user_id: str, filename: str) -> Optional[str]:
        """Get file path for a user's document"""
        possible_paths = [
            f"{self.base_path}/resumes/{filename}",
            f"{self.base_path}/photos/{filename}",
            f"{self.base_path}/certificates/{filename}",
            f"{self.base_path}/{filename}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    async def delete_document(self, user_id: str, filename: str) -> bool:
        """Delete a user's document"""
        file_path = await self.get_document_path(user_id, filename)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    async def list_user_documents(self, user_id: str) -> List[dict]:
        """List all documents for a user"""
        documents = []
        
        # Check all document directories
        directories = ["resumes", "photos", "certificates", ""]
        
        for directory in directories:
            dir_path = f"{self.base_path}/{directory}" if directory else self.base_path
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if filename.startswith(user_id + "_"):
                        file_path = os.path.join(dir_path, filename)
                        stat = os.stat(file_path)
                        
                        doc_type = "unknown"
                        if directory == "resumes":
                            doc_type = "resume"
                        elif directory == "photos":
                            doc_type = "photo"
                        elif directory == "certificates":
                            doc_type = "certificate"
                        
                        documents.append({
                            "filename": filename,
                            "document_type": doc_type,
                            "file_path": file_path,
                            "file_size": stat.st_size,
                            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
                        })
        
        return documents
    
    async def cleanup_old_documents(self, days_old: int = 30):
        """Clean up documents older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getctime(file_path) < cutoff_time:
                    os.remove(file_path)
