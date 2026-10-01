# Example Python Code for CRUD operations

from pymongo import MongoClient 
from bson.objectid import ObjectId 


class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'I<3mongo' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    def create(self, data: dict) -> bool: 
        """Inserts a single document into the specified collection.
        
        Args:
            data (dict): Key/value pairs representing the document to insert
            
        Returns:
            bool: True if insertion is acknowledged by MongoDB, else False.
        """
        # validate data is non-empty dict
        if isinstance(data, dict) and data: 
            try:
                # insert document into the collection
                result = self.collection.insert_one(data)
                
                # returns acknowledgment status from MongoDB
                return bool(result.acknowledged)
            
            except Exception as e: 
                print(f"An error occurred during [C]RUD- CREATE: {e}")
                return False
        else:
            return False

    def read(self, query: dict) -> list: 
        """Query for document(s) in the collection using find().
        
        Args:
            query (dict): Lookup key/value pair(s) used to filter matching documents
                An empty dictionary ({}) retrieves all documents
                
        Returns: 
            list: List of matching documents, or an empty list on failure
        """
        # Validate query is a dict (allowing {} for all documents)
        if isinstance(query, dict):
            try:
                # find() returns unexhausted PyMongo cursor
                cursor = self.collection.find(query)
                
                # Exhaust cursor into native Python list
                return list(cursor) 
            
            except Exception as e:
                print(f"An error occurred during C[R]UD- READ: {e}")
                return []
        else:
            return []
    
    def update(self, query: dict, update_data: dict) -> int: 
        """Query for and modify document(s) in the collection.
        
        Args:
            query (dict): Lookup key/value pair(s) used to filter matching documents
            update_data (dict): Key/value pairs containing modifications
        
        Returns: 
            int : The number of documents modified in the collection
        """
        # Validate both query criteria and update data are non-null dictionaries
        if (
            isinstance(query, dict)
            and isinstance(update_data, dict)
            and update_data
        ):
            try: 
                # wrap update_data in $set if atomic operators are omitted
                if not any(key.startswith("$") for key in update_data.keys()):
                    update_payload = {"$set": update_data}
                else:
                    update_payload = update_data
                
                # Execute update across matching documents
                result = self.collection.update_many(query, update_payload)
                
                # Return count of modified documents upon success
                return result.modified_count
            
            except Exception as e:
                # handle query errors
                print(f"An error occurred during CR[U]D- UPDATE: {e}")
                return 0
        else: 
            return 0
        
    def delete(self, query:dict) -> int:  
        """Query for and remove document(s) from the collection. 
        
        Args: 
            query (dict): Lookup key/value pair(s) used to filter documents for removal.
            
        Returns:
            int: The number of documents removed from the collection
        """
        # Validate that query is a non-empty dictionary to avoid wiping the collection
        if isinstance(query, dict) and query:
            try:
                # Execute deletion across all matching documents
                result = self.collection.delete_many(query)
                
                # Return count of removed documents upon success
                return result.deleted_count
            
            except Exception as e:
                print(f"An error occurred during CRU[D]- DELETE: {e}")
                return 0
        else: 
            return 0
