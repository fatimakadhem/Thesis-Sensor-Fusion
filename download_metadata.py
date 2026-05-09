import json
import re

def main():
    path = r"C:\Users\FAKA0032\Downloads\Thesis-project\dataset\trainval-sequences-full.json"
    
    try:
        print("Läser in den stora filen... vänta...")
        with open(path, 'r') as f:
            # Vi läser hela filen som en enda stor textsträng för att vara säkra
            raw_data = f.read().lower()
        
        print("Skannar efter väderförhållanden...")
        
        # Vi letar efter ZOD:s officiella väderkategorier
        categories = ["clear", "cloudy", "rain", "snow", "fog"]
        stats = {}
        
        for cat in categories:
            # Vi letar efter ordet i citattecken för att vara säkra på att det är ett värde
            count = len(re.findall(f'"{cat}"', raw_data))
            if count > 0:
                stats[cat.upper()] = count

        if not stats:
            print("\nIngen väderdata hittades i den stora JSON-filen.")
            print("Detta bekräftar att du MÅSTE ladda ner 'object_detection' annoteringarna.")
        else:
            print("\n=== DIN VÄDERSTATISTIK (HITTAD I RÅTEXT) ===")
            for weather, count in stats.items():
                print(f"{weather}: {count} st")
            print("============================================")
            print(f"Totalt hittade labels: {sum(stats.values())}")

    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    main()