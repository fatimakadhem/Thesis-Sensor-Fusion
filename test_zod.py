import os
from zod import ZodSequences

# Din sökväg (dubbelkollad)
path = r"C:\Users\FAKA0032\Downloads\Thesis-project\dataset"

try:
    zod_seq = ZodSequences(path, version='full')
    # Vi testar att hämta metadata för den sekvensen du hittade
    meta = zod_seq['000064'].metadata
    print("-" * 30)
    print(f"FRAMGÅNG!")
    print(f"Väder: {meta.weather}")
    print(f"Ljusförhållanden: {meta.time_of_day}")
    print("-" * 30)
except Exception as e:
    print("-" * 30)
    print(f"DET GICK INTE: {e}")
    print("-" * 30)