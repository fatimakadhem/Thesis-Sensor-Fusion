import numpy as np
import pandas as pd
from pathlib import Path
import json

# Bas-sökväg till dina sekvenser
BASE_PATH = Path(r'C:\Users\FAKA0032\Downloads\Thesis-project\dataset\annotations\sequences')

def get_radar_data(seq_id):
    """Laddar radar-punkter och konverterar till x, y (meter)."""
    radar_dir = BASE_PATH / seq_id / "radar"
    files = list(radar_dir.glob("*.npy"))
    if not files:
        return None
    
    # Vi tar den första radarfilen för sekvensen
    data = np.load(files[0])
    
    # Konvertering från polära till kartesiska koordinater
    x = data['radar_range'] * np.cos(data['azimuth_angle'])
    y = data['radar_range'] * np.sin(data['azimuth_angle'])
    
    return pd.DataFrame({
        'x': x, 
        'y': y, 
        'v': data['range_rate'], 
        'amp': data['amplitude']
    })

def get_camera_objects(seq_id):
    """Laddar kamera-detektioner från JSON och filtrerar rörliga klasser."""
    json_path = BASE_PATH / seq_id / "annotations" / "object_detection.json"
    if not json_path.exists():
        return [], {}
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # ZOD JSON kan vara en dict med metadata eller en ren lista
    metadata = {}
    objects = []
    
    if isinstance(data, dict):
        metadata = data.get('metadata', {})
        objects = data.get('objects', []) # Justera om ZOD använder annan nyckel
    else:
        objects = data

    target_classes = ['Vehicle', 'Pedestrian', 'Cyclist', 'Truck', 'Bus']
    relevant = []
    
    for obj in objects:
        obj_class = obj['properties'].get('class')
        if obj_class in target_classes:
            pos = obj['properties']['location_3d']['coordinates']
            relevant.append({
                'class': obj_class, 
                'x': pos[0], 
                'y': pos[1],
                'uuid': obj['properties'].get('annotation_uuid')
            })
    return relevant, metadata

def perform_matching(seq_id, threshold=5.0):
    """Matchar radar-punkter mot kamera-objekt."""
    radar_df = get_radar_data(seq_id)
    camera_objs, metadata = get_camera_objects(seq_id)
    
    if radar_df is None or not camera_objs:
        return None

    results = []
    
    for cam_obj in camera_objs:
        # Beräkna avstånd mellan detta kameraobjekt och ALLA radarpunkter
        dist = np.sqrt((radar_df['x'] - cam_obj['x'])**2 + (radar_df['y'] - cam_obj['y'])**2)
        
        # Hitta träffar inom radien (threshold)
        matches = radar_df[dist <= threshold]
        
        results.append({
            'seq_id': seq_id,
            'class': cam_obj['class'],
            'cam_x': cam_obj['x'],
            'cam_y': cam_obj['y'],
            'radar_matches': len(matches),
            'detected_by_radar': len(matches) > 0,
            # Vi sparar medelvärdet av hastigheten om vi fick en träff
            'avg_radar_v': matches['v'].mean() if len(matches) > 0 else 0
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    # Testa med din sekvens
    seq = "001472"
    print(f"Analyserar sekvens {seq} med threshold 5.0m...")
    
    match_df = perform_matching(seq, threshold=5.0)
    
    if match_df is not None:
        print("\n--- MATCHNINGSRESULTAT ---")
        print(match_df[['class', 'cam_x', 'cam_y', 'radar_matches', 'detected_by_radar']])
        
        total = len(match_df)
        found = match_df['detected_by_radar'].sum()
        print(f"\nResultat: Radar hittade {found} av {total} objekt ({found/total:.1%})")
    else:
        print("Kunde inte genomföra matchning. Kontrollera filsökvägar.")