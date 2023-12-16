import os

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter
from faker import Faker

fake = Faker()
load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
qdrant_token = os.getenv('QDRANT_TOKEN')
qdrant_collection_name = os.getenv('COLLECTION_NAME')


def connect_quadrant():
    """
    Connect to the Quadrant Cloud
    :return:
    """
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_token,
    )
    print(client)
    return client


def create_collection(collection_name):
    """
    Create a collection on the Quadrant Cloud
    :param collection_name:
    :return:
    """
    client = connect_quadrant()

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=100, distance=Distance.COSINE),
    )


def close_connection():
    client = connect_quadrant()
    client.close()


def generate_fake_data(num_points, dimension):
    """
    Generate fake data using Faker and NumPy.
    :param num_points:
    :param dimension:
    """
    fake_data = np.random.random((num_points, dimension))
    return fake_data.tolist()


def add_points_to_qdrant(qdrant_client, vectors):
    """
    Add points to Qdrant using QdrantClient.
    :param qdrant_client:
    :param vectors:
    """
    for vector in vectors:
        payload = {
            "collection_name": "your_collection_name",
            "vectors": [vector],
        }
        response = qdrant_client.insert(collection_name=payload['collection_name'], payload=payload)
        # Handle the response as needed
        print(response)


def search_vector(collection_name):
    """
    Search Vector by collection_name
    :param collection_name:
    :return:
    """
    client = connect_quadrant()
    query_vector = np.random.rand(100)
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5  # Return 5 closest points
    )
    print(hits)
    return hits


def search_with_filter(collection_name: str, key_name: str, query: str):
    """
    Search Vector by collection_name with key_name and query
    :param collection_name:
    :param key_name:
    :param query:
    :return:
    """
    query_vector = np.random.rand(100)
    client = connect_quadrant()
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=Filter(
            must=[
                {"key": key_name, "match": {"value": query}}
            ]
        ),
        limit=1  # Return 5 closest points
    )

    print(hits)
    return hits


def delete_collection(collection_name):
    """
    Delete collection by collection_name
    :param collection_name:
    :return:
    """
    client = connect_quadrant()
    operation = client.delete_collection(collection_name=collection_name)
    if not operation:
        raise Exception(f"Not collection with this name:{collection_name} founded")

    print(f"({collection_name} deleted with success)")
    return operation
