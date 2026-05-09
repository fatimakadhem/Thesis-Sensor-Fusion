import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 1. Ladda data
input_file = "final_thesis_results_summary.csv"
df = pd.read_csv(input_file)
fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
if not os.path.exists(fig_dir): os.makedirs(fig_dir)

summary = df.groupby("Condition").mean()

def add_styling(ax, title):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 9), 
                    textcoords='offset points', fontsize=10, fontweight='bold')
    ax.set_yticks(np.arange(0, 1.1, 0.05))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title(title, fontsize=14)
    plt.ylim(0, 1.05)

# --- FIGUR 1: RADAR ---
plt.figure(figsize=(9, 6))
ax1 = summary['Radar_Acc'].plot(kind='bar', color='#66b3ff', edgecolor='black')
add_styling(ax1, 'Baseline: Radar Accuracy per Road Condition')
plt.savefig(os.path.join(fig_dir, "07_radar_only.png"))
plt.close() # Stänger ner så nästa kan skapas

# --- FIGUR 2: KAMERA ---
plt.figure(figsize=(9, 6))
ax2 = summary['Camera_Acc'].plot(kind='bar', color='#ff9999', edgecolor='black')
add_styling(ax2, 'Baseline: Camera Accuracy per Road Condition')
plt.savefig(os.path.join(fig_dir, "07_camera_only.png"))
plt.close()

# --- FIGUR 3: JÄMFÖRELSE ---
plt.figure(figsize=(11, 7))
ax3 = summary[['Camera_Acc', 'Radar_Acc', 'Fused_Acc']].plot(kind='bar', color=['#ff9999', '#66b3ff', '#99ff99'], edgecolor='black')
add_styling(ax3, 'Comparison: Sensors vs Weighted Fusion')
plt.legend(["Camera", "Radar", "Weighted Fusion"], loc='lower left')
plt.savefig(os.path.join(fig_dir, "07_comparison_all.png"))
plt.close()

print("Succé! Gå till mappen 'figures' nu, där ligger '07_camera_only.png' och väntar på dig.")