from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np

class FileAnalyzer:
    def __init__(self, n_clusters=4, risk_weights=None):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.weights = risk_weights or {'size': 0.3, 'age': 0.5, 'access': 0.2}

    def cluster_files(self, df):
        features = ['size_log', 'days_since_mod', 'days_since_accessed', 'path_depth']
        X_scaled = self.scaler.fit_transform(df[features])
        df['cluster'] = self.model.fit_predict(X_scaled)
        
        # Model Validation (Crucial for Interviews)
        self.silhouette = float(silhouette_score(X_scaled, df['cluster']))
        
        # Cluster Profiling & Decision-Ready Labeling
        self.cluster_profiles = self._generate_profiles(df)
        df['cluster_label'] = df['cluster'].map({k: v['label'] for k, v in self.cluster_profiles.items()})
        
        # Risk Score Calculation (Weighted Formula)
        df['risk_score'] = self._calculate_risk(df)
        return df

    def _calculate_risk(self, df):
        def norm(col): 
            return (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-9)
        
        return (
            norm('size_log') * self.weights.get('size', 0.3) +
            norm('days_since_mod') * self.weights.get('age', 0.5) +
            norm('days_since_accessed') * self.weights.get('access', 0.2)
        ).round(3)

    def _generate_profiles(self, df):
        profiles = df.groupby('cluster').agg({
            'size_kb': 'median', 'days_since_mod': 'median'
        }).to_dict('index')
        
        age_mid = df['days_since_mod'].median()
        size_mid = df['size_kb'].median()

        for k, v in profiles.items():
            if v['days_since_mod'] > age_mid and v['size_kb'] > size_mid:
                v['label'] = "Dormant Giants (High Risk)"
            elif v['days_since_mod'] < age_mid and v['size_kb'] > size_mid:
                v['label'] = "Active Large Files"
            elif v['days_since_mod'] > age_mid:
                v['label'] = "Small Stale Artifacts"
            else:
                v['label'] = "Active Workspace"
        return profiles

    def get_action_items(self, df):
        # Top 5% statistically highest risk files
        return df[df['risk_score'] >= df['risk_score'].quantile(0.95)].sort_values(by='risk_score', ascending=False)