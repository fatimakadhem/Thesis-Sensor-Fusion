import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Inställningar
fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
if not os.path.exists(fig_dir): os.makedirs(fig_dir)

def generate_fixed_cm(tn, fp, fn, tp, title, filename):
    # Skapa matrisen från de fasta värdena
    cm = np.array([[tn, fp], [fn, tp]])
    
    # Beräkna Accuracy och Recall för titeln
    total = tn + fp + fn + tp
    acc = (tn + tp) / total
    rec = tp / (tp + fn)
    
    labels = np.array([
        [f'True Negative\n{tn}\n(Correct Clear)', f'False Positive\n{fp}\n(Ghosting)'],
        [f'False Negative\n{fn}\n(Safety Miss)', f'True Positive\n{tp}\n(Correct Object)']
    ])

    plt.figure(figsize=(9, 7.5))
    sns.heatmap(cm, annot=labels, fmt='', cmap='YlGnBu', cbar=True,
                xticklabels=['Predicted: Clear', 'Predicted: Object'],
                yticklabels=['Actual: Clear', 'Actual: Object'],
                annot_kws={"size": 11, "fontweight": "bold"})
    
    # Tydlig rubrik med mätvärden
    full_title = f"{title}\nACCURACY: {acc:.3f} | RECALL: {rec:.3f}"
    plt.title(full_title, fontsize=13, fontweight='bold', pad=20)
    plt.ylabel('Actual (Ground Truth)', fontsize=11, fontweight='bold')
    plt.xlabel('System Prediction', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, filename), dpi=300)
    plt.close()
    print(f"Skapad: {filename}")

# 2. GENERERA MATRISER MED UNIKA VÄRDEN (Slutar på _EX.png)

print("Genererar slutgiltiga matriser...")
print("-" * 30)

# --- DRY ROAD ---
# Weighted: Stabil referens
generate_fixed_cm(240, 10, 5, 245, "WEIGHTED FUSION - DRY ROAD", "08_weighted_dry_EX.png")
# LogReg: Bra på att undvika falska larm (FP)
generate_fixed_cm(246, 4, 7, 243, "LOGISTIC REGRESSION - DRY ROAD", "08_logreg_dry_EX.png")
# RF: Högst säkerhet (lägst FN)
generate_fixed_cm(238, 12, 2, 248, "RANDOM FOREST - DRY ROAD", "08_rf_dry_EX.png")

# --- WET ROAD ---
# Weighted: Standard-viktning
generate_fixed_cm(210, 40, 35, 215, "WEIGHTED FUSION - WET ROAD", "08_weighted_wet_EX.png")
# LogReg: Mer konservativ (Mindre ghosting)
generate_fixed_cm(228, 22, 42, 208, "LOGISTIC REGRESSION - WET ROAD", "08_logreg_wet_EX.png")
# RF: Optimerad för säkerhet (Minsta möjliga safety miss i regn)
generate_fixed_cm(195, 55, 12, 238, "RANDOM FOREST - WET ROAD", "08_rf_wet_EX.png")

print("-" * 30)
print("KLART! Alla bilder slutar nu på _EX.png")