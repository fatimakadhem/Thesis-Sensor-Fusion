import json
from pathlib import Path

BASE_PATH = Path(r'C:\Users\FAKA0032\Downloads\Thesis-project\dataset\annotations\sequences')

def get_moving_objects(sequence_id):
    json_path = BASE_PATH / sequence_id / "annotations" / "object_detection.json"
    
    if not json_path.exists():
        return []

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Intressanta klasser för fusion av rörliga objekt
    target_classes = ['Vehicle', 'Pedestrian', 'Cyclist', 'Truck', 'Bus']
    
    relevant_objects = []
    for obj in data:
        obj_class = obj['properties'].get('class')
        if obj_class in target_classes:
            # Spara ner viktig info för fusionen
            relevant_objects.append({
                'class': obj_class,
                'pos_3d': obj['properties']['location_3d']['coordinates'], # [x, y, z]
                'uuid': obj['properties']['annotation_uuid']
            })
            
    return relevant_objects

if __name__ == "__main__":
    test_id = "001472"
    moving_objs = get_moving_objects(test_id)
    
    print(f"Hittade {len(moving_objs)} potentiellt rörliga objekt i sekvens {test_id}:")
    for o in moving_objs[:3]: # Visa de 3 första
        print(f"- {o['class']} vid position: {o['pos_3d']}")