import os

import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter

load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
qdrant_token = os.getenv('QDRANT_TOKEN')
collection_name = os.getenv('COLLECTION_NAME')


def connect_quadrant():
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_token,
    )
    print(client)
    return client


def create_collection():
    client = connect_quadrant()

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=100, distance=Distance.COSINE),
    )


def close_connection():
    client = connect_quadrant()

    client.close()


def create_vector(payload):
    client = connect_quadrant()

    vectors = np.random.rand(100, 100)
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload=payload
            )
            for idx, vector in enumerate(vectors)
        ]
    )


def update_collection(payload_list):
    for payload in payload_list:
        create_vector(payload)


def search_vector():
    client = connect_quadrant()
    query_vector = np.random.rand(100)
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5  # Return 5 closest points
    )
    print(hits)
    return hits


def search_with_filter(query: str):
    query_vector = np.random.rand(100)
    client = connect_quadrant()
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=Filter(
            must=[
                {"key": "name", "match": {"value": query}}
            ]
        ),
        limit=1  # Return 5 closest points
    )

    print(hits)
