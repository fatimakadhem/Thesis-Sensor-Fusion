import os
from pathlib import Path

# Sökvägen till där dina 1400 mappar bor
base_path = Path(r'C:\Users\FAKA0032\Downloads\Thesis-project\dataset\annotations\sequences')

def check_dataset():
    if not base_path.exists():
        print(f"FEL: Hittar inte mappen {base_path}")
        return

    # Räkna alla undermappar
    sequences = [d for d in base_path.iterdir() if d.is_dir()]
    print(f"Antal sekvenser hittade: {len(sequences)}")

    # Kolla i en specifik mapp (t.ex. 000064)
    test_folder = base_path / "000064" / "radar"
    if test_folder.exists():
        files = list(test_folder.glob('*'))
        print(f"I mapp 000064 hittades {len(files)} radarfiler.")
    else:
        print("Kunde inte hitta radar-undermappen i 000064.")

if __name__ == "__main__":
    check_dataset()