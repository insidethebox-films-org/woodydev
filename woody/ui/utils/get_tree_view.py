from pymongo import MongoClient

tree_dict = {}

client = MongoClient("mongodb://100.113.50.90:2222/")

db = client["test"]

root_level = ["assets", "shots"]

def get_groups_sequences():

    collections = ["groups", "sequences"]
    results = {}

    for collection_name in collections:
        documents = list(db[collection_name].find({}, {"name": 1, "_id": 0}))
        results[collection_name] = [doc["name"] for doc in documents]

    return results["groups"], results["sequences"]

def get_assets_shots():

    collections = ["assets", "shots"]
    results = {}

    for collection_name in collections:
        documents = list(db[collection_name].find({}, {"name": 1, "group": 1, "sequence": 1, "_id": 0}))
        results[collection_name] = [doc for doc in documents]

    return results["assets"], results["shots"]


def build_tree_data():
    groups, sequences = get_groups_sequences()
    assets, shots = get_assets_shots()
    
    # Build assets tree
    assets_tree = {
        'name': 'assets',
        'children': []
    }
    
    # Group assets by their group
    for group in groups:
        group_assets = [asset['name'] for asset in assets if asset.get('group') == group]
        if group_assets:
            assets_tree['children'].append({
                'name': group,
                'children': group_assets
            })
    
    # Build shots tree
    shots_tree = {
        'name': 'shots', 
        'children': []
    }
    
    # Group shots by their sequence
    for sequence in sequences:
        sequence_shots = [shot['name'] for shot in shots if shot.get('sequence') == sequence]
        if sequence_shots:
            shots_tree['children'].append({
                'name': sequence,
                'children': sequence_shots
            })
    
    return [assets_tree, shots_tree]


groups, sequences = get_groups_sequences()
assets, shots = get_assets_shots()

print(groups, sequences, assets, shots)
print("\nTree structure:")
tree_data = build_tree_data()
print(tree_data)