import yaml
import json
import os
import shutil
from src.extractor import MetadataExtractor
from src.processor import DataProcessor
from src.analyzer import FileAnalyzer
from src.visualizer import DataVisualizer

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 1. Extraction
    print(f"🚀 Scanning: {config['scan_settings']['root_directory']}...")
    raw_df = MetadataExtractor(config['scan_settings']['root_directory'], 
                               config['scan_settings']['exclude_extensions']).run()
    
    # 2. Adaptive Feature Engineering
    print("⚙️ Engineering statistical features...")
    processed_df = DataProcessor.clean_and_feature_engineer(raw_df)

    # 3. ML Intelligence & Scoring
    print("🤖 Clustering behavioral patterns & scoring risk...")
    analyzer = FileAnalyzer(n_clusters=config['ml_settings']['n_clusters'], 
                            risk_weights=config['ml_settings']['risk_weights'])
    final_df = analyzer.cluster_files(processed_df)

    # 4. PERSISTENCE LAYER: JSON (Executive Summary)
    intelligence_summary = {
        "model_validation": {"silhouette_score": analyzer.silhouette},
        "cluster_profiles": analyzer.cluster_profiles,
        "system_health": {
            "total_files": len(final_df),
            "high_risk_threshold": float(final_df['risk_score'].quantile(0.95))
        }
    }
    with open("intelligence_summary.json", "w") as f:
        json.dump(intelligence_summary, f, indent=4)

    # 5. PERSISTENCE LAYER: CSV (Raw + Enriched Dataset for BI tools)
    final_df.to_csv("intelligence_report.csv", index=False)

    # 6. PERSISTENCE LAYER: PNG (Dashboard)
    DataVisualizer.generate_dashboard(final_df)

    # Output to CLI
    candidates = analyzer.get_action_items(final_df)
    print("\n" + "!"*60 + "\nCORE SYSTEM INTELLIGENCE SUMMARY\n" + "!"*60)
    print(f"[DECISION]: Identified {len(candidates)} high-risk files for archival.")
    print(candidates[['file_name', 'cluster_label', 'risk_score']].head(5).to_string(index=False))
    
    print(f"\n✅ Audit Complete. Silhouette Score: {analyzer.silhouette:.2f}")

if __name__ == "__main__":
    main()