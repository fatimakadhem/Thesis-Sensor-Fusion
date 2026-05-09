import pandas as pd
import matplotlib.pyplot as plt
import os

# Vi letar efter filen i samma mapp som scriptet
input_file = os.path.join(os.path.dirname(__file__), "final_thesis_results_summary.csv")

if not os.path.exists(input_file):
    print(f"FEL: Hittade inte {input_file}")
else:
    df = pd.read_csv(input_file)
    summary = df.groupby("Condition").mean()

    print("--- DATA HITTAD FÖR GRAF ---")
    print(summary)

    ax = summary.plot(kind='bar', figsize=(10, 6), color=['#ff9999','#66b3ff','#99ff99'])
    plt.title('Sensor Fusion Performance under different Road Conditions')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.0)
    
    # Skapa figures-mappen om den saknas
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    if not os.path.exists(fig_dir): os.makedirs(fig_dir)
    
    plt.savefig(os.path.join(fig_dir, "fusion_chart.png"))
    plt.show()