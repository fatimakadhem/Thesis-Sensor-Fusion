import numpy as np
from pathlib import Path

def get_radar_path(sequence_id):
    """Hittar .npy-filen för en specifik sekvens (t.ex. '000064')"""
    base_dir = Path(r'C:\Users\FAKA0032\Downloads\Thesis-project\dataset\annotations\sequences')
    radar_dir = base_dir / sequence_id / "radar"
    
    if not radar_dir.exists():
        return None
    
    # Hämtar första .npy filen i mappen
    files = list(radar_dir.glob("*.npy"))
    return files[0] if files else None

def load_radar_data(sequence_id):
    path = get_radar_path(sequence_id)
    if path:
        return np.load(path)
    print(f"Kunde inte hitta radar-fil för {sequence_id}")
    return None

if __name__ == "__main__":
    # Testkör för sekvens 000064
    data = load_radar_data("000064")
    if data is not None:
        print(f"Laddade {len(data)} punkter från sekvens 000064")