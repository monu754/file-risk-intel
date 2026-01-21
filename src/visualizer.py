import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    @staticmethod
    def generate_dashboard(df):
        sns.set_theme(style="darkgrid")
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('System Intelligence & Risk Audit Dashboard', fontsize=22, fontweight='bold')

        # 1. Decision Logic (Risk Score vs Age)
        sns.scatterplot(ax=axes[0, 0], data=df, x='days_since_mod', y='risk_score', 
                        hue='cluster_label', palette='rocket', alpha=0.7)
        axes[0, 0].set_title("Risk Profile by Cluster (Behavioral Segmentation)")

        # 2. Total Storage Impact
        impact = df.groupby('cluster_label')['size_kb'].sum() / 1024
        impact.sort_values().plot(kind='barh', ax=axes[0, 1], color='teal')
        axes[0, 1].set_title("Storage Impact (MB) per Behavioral Segment")

        # 3. Decision Queue (Top 5 Risk Files)
        axes[1, 0].axis('off')
        top_risk = df.nlargest(5, 'risk_score')[['file_name', 'risk_score', 'cluster_label']]
        table = axes[1, 0].table(cellText=[["File", "Score", "Label"]] + top_risk.values.tolist(), 
                                 loc='center', cellLoc='left')
        table.set_fontsize(12)
        axes[1, 0].set_title("Immediate Action Queue (Highest Precision Risk)")

        # 4. Corrected Boxplot (No Warnings)
        sns.boxplot(ax=axes[1, 1], x='cluster_label', y='days_since_mod', data=df, 
                    hue='cluster_label', palette="Set2", legend=False)
        plt.setp(axes[1, 1].get_xticklabels(), rotation=15)
        axes[1, 1].set_title("Age Variance across Clusters")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig("system_risk_audit.png", dpi=300)
        plt.close()