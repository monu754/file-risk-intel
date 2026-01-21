import pandas as pd
import numpy as np
import os
from datetime import datetime

class DataProcessor:
    @staticmethod
    def clean_and_feature_engineer(df):
        if df.empty: return df
        now = datetime.now()
        
        # Temporal Features (Raw)
        df['days_since_mod'] = (now - df['mtime']).dt.days
        df['days_since_created'] = (now - df['ctime']).dt.days
        df['days_since_accessed'] = (now - df['atime']).dt.days
        df['hour_created'] = df['ctime'].dt.hour
        
        # Statistical Thresholding (Adaptive Intelligence)
        # Defining 'Stale' as the 75th percentile of age in THIS system
        stale_threshold = df['days_since_mod'].quantile(0.75)
        df['is_stale'] = df['days_since_mod'] > stale_threshold
        
        # Scaling & Structural Signals
        df['size_log'] = np.log1p(df['size_kb'])
        df['path_depth'] = df['file_path'].apply(lambda x: len(x.split(os.sep)))
        
        return df