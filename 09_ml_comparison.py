import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score

# 1. Inställningar och mappar
input_file = "final_thesis_results_summary.csv"
if not os.path.exists(input_file):
    print("Fel: Kör 05_analysis_fusion.py först för att skapa datagrunden!")
    exit()

df = pd.read_csv(input_file)
fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
if not os.path.exists(fig_dir): os.makedirs(fig_dir)

# 2. SKAPA TRÄNINGSDATA (Nu mer realistisk med 2000 prover)
np.random.seed(42)
n_samples = 2000 
actual = np.random.randint(0, 2, n_samples)
conditions = np.random.choice(['Dry', 'Wet'], n_samples)

# Hämta dina faktiska noggrannhetsvärden
cam_dry_acc = df[df['Condition']=='Dry']['Camera_Acc'].values[0]
cam_wet_acc = df[df['Condition']=='Wet']['Camera_Acc'].values[0]
rad_acc = 0.85 

cam_input = []
rad_input = []

for i in range(n_samples):
    c_acc = cam_dry_acc if conditions[i] == 'Dry' else cam_wet_acc
    # Sensorerna simuleras med brus för att ge ML-modellen något att "lösa"
    cam_input.append(actual[i] if np.random.random() < c_acc else 1 - actual[i])
    rad_input.append(actual[i] if np.random.random() < rad_acc else 1 - actual[i])

X = pd.DataFrame({'Camera': cam_input, 'Radar': rad_input})
y = actual

# 3. TRÄNA MODELLERNA
log_reg = LogisticRegression().fit(X, y)
rf = RandomForestClassifier(n_estimators=100, max_depth=5).fit(X, y)

# --- BERÄKNA REALTIDSMÄTVÄRDEN ---
acc_rf = rf.score(X, y)
y_pred_rf = rf.predict(X)
recall_rf = recall_score(y, y_pred_rf)

acc_log = log_reg.score(X, y)
y_pred_log = log_reg.predict(X)      # <--- LAGT TILL FÖR RECALL
recall_log = recall_score(y, y_pred_log) # <--- LAGT TILL FÖR RECALL
# --------------------------------

# 4. SKAPA SANNOLIKHETSTABELLEN (För de första 10 raderna)
probs_lr = log_reg.predict_proba(X[:10])[:, 1]
probs_rf = rf.predict_proba(X[:10])[:, 1]

results_table = pd.DataFrame({
    'Actual Object': y[:10],
    'ML Prob (LogReg)': probs_lr.round(3),
    'ML Prob (RandForest)': probs_rf.round(3)
})

# 5. SPARA TABELLEN SOM BILD
fig, ax = plt.subplots(figsize=(10, 7))
ax.axis('off')
table = ax.table(cellText=results_table.values, colLabels=results_table.columns, 
                  loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 2.0)

# UPPDATERAD TITEL FÖR ATT VISA ALLA VÄRDEN I BILDEN
plt.title(f"ML Sensor Fusion Comparison\n\n"
          f"Logistic Reg - Acc: {acc_log:.3f}, Recall: {recall_log:.3f}\n"
          f"Random Forest - Acc: {acc_rf:.3f}, Recall: {recall_rf:.3f}", 
          fontsize=12, fontweight='bold', pad=30)

plt.savefig(os.path.join(fig_dir, "09_ml_comparison_final.png"), bbox_inches='tight', dpi=300)

# 6. TERMINAL OUTPUT
print("\n" + "="*30)
print("       ANALYS KLAR")
print("="*30)
print(f"Logistic Regression Acc:    {acc_log:.4f}")
print(f"Logistic Regression Recall: {recall_log:.4f}")
print(f"Random Forest Accuracy:     {acc_rf:.4f}")
print(f"Random Forest Recall:       {recall_rf:.4f}")
print("-"*30)
print("Sannolikhetstabell (urval):")
print(results_table)
print(f"\nNy bild sparad: figures/09_ml_comparison_final.png")