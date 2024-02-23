import os
#from dotenv import load_dotenv
#from chromadb.config import Settings
import chromadb

#load_dotenv()

# Define the folder for storing database
PERSIST_DIRECTORY = 'C:\\Users\\tarun\\chrome_db_data' #os.environ.get('PERSIST_DIRECTORY')



COLLETION_NAME = 'private_content_type4'

#chroma_client = chromadb.Client(CHROMA_SETTINGS)
chroma_client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

chroma_collection = chroma_client.get_or_create_collection(name=COLLETION_NAME, metadata={"hnsw:space": "cosine"})


