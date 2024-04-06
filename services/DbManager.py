import pymongo.errors
from pymongo import MongoClient
from datetime import datetime


class MongoManager:
    def __init__(self):
        """
        Initialize MongoDB connection.

        :param db_name: Name of the database to use.
        :param collection_name: Name of the collection to use.
        :param host: Hostname where MongoDB is running.
        :param port: Port number on which MongoDB is listening.
        """
        try:
            db_name = "BureauFraudDetection"
            collection_name = "Transaction"
            self.client = MongoClient(host='localhost', port=27017)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except pymongo.errors.ConnectionFailure as e:
            print("Cannot Connect to MongoDB")

    def add_document(self, document):
        """
        Add a single document to the collection.

        :param document: A dictionary representing the document to add.
        :return: The ID of the inserted document.
        """
        self.collection.insert_one(document)

    def get_past_transactions(self,startDate, endDate):

        # Query to find documents within the time range
        query_result = self.collection.find({
            'dateTimeTransaction': {
                '$gte': startDate,
                '$lte': endDate
            }
        })
        doc_list = []
        # Print the documents found
        for document in query_result:
            doc_list.append(document)

        if (len(doc_list) == 0):
            return []
        else:
            return doc_list
