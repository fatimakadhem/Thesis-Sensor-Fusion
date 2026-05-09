import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# 1. Inställningar och mappar
input_file = "final_thesis_results_summary.csv"
if not os.path.exists(input_file):
    print("Fel: Kör 05_analysis_fusion.py först för att skapa datagrunden!")
    exit()

df = pd.read_csv(input_file)
fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
if not os.path.exists(fig_dir): os.makedirs(fig_dir)

# 2. SKAPA TRÄNINGSDATA (Baserat på din riktiga sensor-prestanda)
# Vi skapar en dataset där ML får lära sig sambanden
np.random.seed(42)
n_samples = 1000
actual = np.random.randint(0, 2, n_samples)
conditions = np.random.choice(['Dry', 'Wet'], n_samples)

# Hämta dina faktiska noggrannhetsvärden från filen
cam_dry_acc = df[df['Condition']=='Dry']['Camera_Acc'].values[0]
cam_wet_acc = df[df['Condition']=='Wet']['Camera_Acc'].values[0]
rad_acc = 0.85 # Standardvärde för radar i din analys

cam_input = []
rad_input = []

for i in range(n_samples):
    # Kameran presterar olika beroende på väder
    c_acc = cam_dry_acc if conditions[i] == 'Dry' else cam_wet_acc
    cam_input.append(actual[i] if np.random.random() < c_acc else 1 - actual[i])
    # Radarn är stabil
    rad_input.append(actual[i] if np.random.random() < rad_acc else 1 - actual[i])

# Skapa Features (X) och Target (y)
X = pd.DataFrame({'Camera': cam_input, 'Radar': rad_input})
y = actual

# 3. TRÄNA MODELLERNA (Inlärningsfasen)
# Här använder vi fit(X, y) för att bygga logiken
log_reg = LogisticRegression().fit(X, y)
rf = RandomForestClassifier(n_estimators=100).fit(X, y)

# 4. SKAPA SANNOLIKHETSTABELLEN (Konfidensgrad)
# Vi tar 10 exempelrader för att visa handledaren
probs_lr = log_reg.predict_proba(X[:10])[:, 1]
probs_rf = rf.predict_proba(X[:10])[:, 1]

results_table = pd.DataFrame({
    'Actual Object': y[:10],
    'ML Prob (LogReg)': probs_lr.round(3),
    'ML Prob (RandForest)': probs_rf.round(3)
})

# 5. SPARA TABELLEN SOM BILD
fig, ax = plt.subplots(figsize=(9, 5))
ax.axis('off')
table = ax.table(cellText=results_table.values, colLabels=results_table.columns, 
                 loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.8)

plt.title("Sensor Fusion: Machine Learning Confidence Levels\n(Training based on Camera vs Radar reliability)", 
          fontsize=14, fontweight='bold', pad=20)

plt.savefig(os.path.join(fig_dir, "09_ml_probability_table.png"), bbox_inches='tight', dpi=300)

print("\n=== TRÄNING KLAR ===")
print(f"Logistic Regression Accuracy: {log_reg.score(X, y):.2f}")
print(f"Random Forest Accuracy: {rf.score(X, y):.2f}")
print("\n--- SANNOLIKHETSTABELL (SPARAD SOM BILD) ---")
print(results_table)
print(f"\nKolla i mappen 'figures' efter: 09_ml_probability_table.png")