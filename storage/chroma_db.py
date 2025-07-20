import chromadb
from config import DATA_DIR

class ChapterDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(DATA_DIR / "chroma_db"))
        self.collection = self.client.get_or_create_collection("book_chapters")
    
    def add_chapter(self, chapter_id, text, metadata):
        """Add chapter to database"""
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[chapter_id]
        )
    
    def search_chapters(self, query, n_results=3):
        """Semantic search for chapters"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results