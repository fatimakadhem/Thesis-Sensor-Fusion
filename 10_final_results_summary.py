import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. SAMMANSTÄLL RESULTATEN
# ==========================================
# Här hårdkodar vi medelvärdena från dina tidigare analyser 
# för att skapa en ren och tydlig slutgraf.
data = {
    'Method': [
        'Camera Only', 
        'Radar Only', 
        'Heuristic Fusion (Manual)', 
        'Logistic Regression (ML)', 
        'Random Forest (ML)'
    ],
    'Accuracy': [
        0.58,  # Snitt för kamera över alla väglag
        0.85,  # Snitt för radar
        0.81,  # Din viktade fusion
        0.88,  # ML Metod 1
        0.92   # ML Metod 2 (Vinnaren!)
    ],
    'Type': ['Baseline', 'Baseline', 'Heuristic', 'Machine Learning', 'Machine Learning']
}

df_final = pd.DataFrame(data)

# ==========================================
# 2. SKAPA DEN SLUTGILTIGA JÄMFÖRELSEGRAFEN
# ==========================================
plt.figure(figsize=(12, 7))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#bcbd22']

bars = plt.bar(df_final['Method'], df_final['Accuracy'], color=colors, edgecolor='black', alpha=0.8)

# Lägg till värden ovanpå staplarna
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f'{yval:.2f}', ha='center', va='bottom', fontweight='bold')

plt.title('Final Performance Comparison: Single Sensors vs. Fusion Methods', fontsize=16, pad=20)
plt.ylabel('System Accuracy (0.0 - 1.0)', fontsize=12)
plt.ylim(0, 1.1) # Lite extra plats för texten ovanpå
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Spara figuren
fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
if not os.path.exists(fig_dir): os.makedirs(fig_dir)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "10_final_comparison_hero.png"))
plt.show()

print("\n" + "="*50)
print("   GRATTIS! DIN SLUTGILTIGA ANALYS ÄR KLAR")
print("="*50)
print("Grafen '10_final_comparison_hero.png' är nu sparad.")
print("Den visar tydligt hur du gått från baseline till optimerad ML-fusion.")
