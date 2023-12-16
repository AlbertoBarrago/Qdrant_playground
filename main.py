from service.quadrant_db import update_collection

if __name__ == '__main__':
    update_collection([{"name": "Phoolvius", "status": "The Cat"},
                       {"name": "Albz", "status": "The Owner"}])
