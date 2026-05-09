import numpy as np
import os

# Sökväg till den fil vi precis hittade
file_path = r'C:\Users\FAKA0032\Downloads\Thesis-project\dataset\annotations\sequences\000064\radar\000064_romeo_FC_2022-01-28T09_53_27331984Z.npy'

def inspect_radar():
    try:
        # Ladda npy-filen
        data = np.load(file_path)
        
        print("--- RADAR DATA INSPEKTION ---")
        print(f"Shape: {data.shape}")
        print(f"Datatyp: {data.dtype}")
        
        # Om det är en strukturerad array (ZOD radar brukar ha kolumnnamn)
        if data.dtype.names:
            print(f"Kolumner: {data.dtype.names}")
            # Visa första 5 raderna
            for i in range(min(5, len(data))):
                print(f"Punkt {i}: {data[i]}")
        else:
            # Om det är en vanlig matris, visa första raden
            print("Första raden (rådata):")
            print(data[0])

    except Exception as e:
        print(f"Kunde inte läsa filen: {e}")

if __name__ == "__main__":
    inspect_radar()