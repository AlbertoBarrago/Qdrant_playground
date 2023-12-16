from service.quadrant_db import create_collection

if __name__ == '__main__':
    print("Hi man, you are on qdrant cli_py :-)")
    collection_name = input("Insert name of new collection:")
    print(f"Creating collection {collection_name}...")
    create_collection(collection_name)
    print(f"Collection {collection_name} created successfully!")

