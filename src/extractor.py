import os
import pandas as pd
from pathlib import Path
from datetime import datetime

class MetadataExtractor:
    def __init__(self, root_path, exclude_exts=None):
        self.root_path = Path(root_path)
        self.exclude_exts = exclude_exts or []

    def run(self):
        file_data = []
        for path in self.root_path.rglob('*'):
            if path.is_file() and path.suffix not in self.exclude_exts:
                try:
                    stats = path.stat()
                    file_data.append({
                        "file_path": str(path),
                        "file_name": path.name,
                        "extension": path.suffix.lower() or "no_ext",
                        "size_kb": stats.st_size / 1024,
                        "ctime": datetime.fromtimestamp(stats.st_ctime),
                        "mtime": datetime.fromtimestamp(stats.st_mtime),
                        "atime": datetime.fromtimestamp(stats.st_atime),
                        "path_depth": len(path.parts)
                    })
                except (PermissionError, FileNotFoundError):
                    continue
        return pd.DataFrame(file_data)