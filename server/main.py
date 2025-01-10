import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv
import hashlib
import json
from datetime import datetime
import logging
import sys

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Configure logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "server.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file in project root
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)
logger.info(f"Loading environment from: {ENV_PATH}")

# Initialize FastAPI app
app = FastAPI(title="TxtAI Assistant MCP",
             description="Memory and semantic search server using TxtAI",
             version="1.0.0")

# Add CORS middleware with configurable origins
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
MEMORY_FILE = DATA_DIR / "memories.json"
TAG_FILE = DATA_DIR / "tags.json"

# In-memory storage with file persistence
memories = {}
tags_index = {}

class Memory(BaseModel):
    content: str
    metadata: Optional[Dict] = {}
    tags: Optional[List[str]] = []
    type: Optional[str] = "general"

class SearchQuery(BaseModel):
    query: str
    n_results: Optional[int] = 5
    similarity_threshold: Optional[float] = 0.7

class TagSearch(BaseModel):
    tags: List[str]

def load_data():
    """Load memories and tags from files if they exist."""
    global memories, tags_index
    try:
        if MEMORY_FILE.exists():
            memories = json.loads(MEMORY_FILE.read_text())
        if TAG_FILE.exists():
            tags_index = {k: set(v) for k, v in json.loads(TAG_FILE.read_text()).items()}
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def save_data():
    """Save memories and tags to files."""
    try:
        MEMORY_FILE.write_text(json.dumps(memories, indent=2))
        # Convert sets to lists for JSON serialization
        tags_json = {k: list(v) for k, v in tags_index.items()}
        TAG_FILE.write_text(json.dumps(tags_json, indent=2))
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise

def generate_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application")
    try:
        load_data()
        logger.info("Server started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.post("/store")
async def store_memory(memory: Memory):
    try:
        logger.info(f"Storing new memory: {memory.content[:100]}...")
        
        content_hash = generate_content_hash(memory.content)
        
        memory_data = {
            "content": memory.content,
            "metadata": memory.metadata,
            "tags": memory.tags,
            "type": memory.type,
            "timestamp": datetime.utcnow().isoformat(),
            "content_hash": content_hash
        }
        
        memories[content_hash] = memory_data
        
        for tag in memory.tags:
            if tag not in tags_index:
                tags_index[tag] = set()
            tags_index[tag].add(content_hash)
        
        save_data()
        logger.info(f"Successfully stored memory with hash: {content_hash}")
        return {"status": "success", "id": content_hash}
    except Exception as e:
        logger.error(f"Error storing memory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_memories(query: SearchQuery):
    try:
        logger.info(f"Searching memories with query: {query.query}")
        results = [
            {
                "content": memory["content"],
                "metadata": memory["metadata"],
                "tags": memory["tags"],
                "type": memory["type"],
                "timestamp": memory["timestamp"],
                "content_hash": memory["content_hash"],
                "similarity_score": 1.0  # Placeholder for actual similarity score
            }
            for memory in memories.values()
        ]
        logger.info(f"Found {len(results)} memories")
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error searching memories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search_tags")
async def search_by_tags(search: TagSearch):
    try:
        logger.info(f"Searching memories by tags: {search.tags}")
        
        memory_sets = [tags_index.get(tag, set()) for tag in search.tags]
        if not memory_sets:
            return {"status": "success", "results": []}
        
        matching_hashes = set.intersection(*memory_sets)
        
        results = []
        for content_hash in matching_hashes:
            if content_hash in memories:
                memory = memories[content_hash]
                results.append({
                    "content": memory["content"],
                    "metadata": memory["metadata"],
                    "tags": memory["tags"],
                    "type": memory["type"],
                    "timestamp": memory["timestamp"],
                    "content_hash": memory["content_hash"]
                })
        
        logger.info(f"Found {len(results)} memories matching tags")
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error searching by tags: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/{content_hash}")
async def delete_memory(content_hash: str):
    try:
        logger.info(f"Attempting to delete memory: {content_hash}")
        
        if content_hash not in memories:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        memory = memories.pop(content_hash)
        
        for tag in memory["tags"]:
            if tag in tags_index:
                tags_index[tag].discard(content_hash)
                if not tags_index[tag]:
                    del tags_index[tag]
        
        save_data()
        logger.info(f"Successfully deleted memory: {content_hash}")
        return {"status": "success", "message": "Memory deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting memory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        logger.info("Retrieving system statistics")
        
        stats = {
            "total_memories": len(memories),
            "total_tags": len(tags_index),
            "tags_distribution": {tag: len(hashes) for tag, hashes in tags_index.items()},
            "memory_types": {},
            "last_added": None
        }
        
        for memory in memories.values():
            memory_type = memory["type"]
            stats["memory_types"][memory_type] = stats["memory_types"].get(memory_type, 0) + 1
            
            if not stats["last_added"] or memory["timestamp"] > stats["last_added"]:
                stats["last_added"] = memory["timestamp"]
        
        logger.info("Successfully retrieved system statistics")
        return {"status": "success", "stats": stats}
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def check_health():
    try:
        logger.info("Performing health check")
        
        health_status = {
            "status": "healthy",
            "memory_store": "operational",
            "total_memories": len(memories),
            "total_tags": len(tags_index),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Health check completed: {health_status['status']}")
        return {"status": "success", "health": health_status}
    except Exception as e:
        logger.error(f"Error during health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting FastAPI server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="debug")
