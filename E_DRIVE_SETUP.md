# VaaniMitra E-Drive Storage Setup

## Overview
VaaniMitra has been configured to store AI models and cache data on your E drive to save space on the C drive.

## Directory Structure
```
E:\VaaniMitraData\
├── models\          # AI model files (~1GB)
│   └── models--ai4bharat--indictrans2-en-indic-dist-200M\
└── cache\           # HuggingFace download cache (~5GB)
    └── models--ai4bharat--indictrans2-en-indic-dist-200M\
```

## Space Savings
- **Before**: ~8GB on C drive (models + cache + virtual env)
- **After**: ~1.7GB on C drive (just virtual environment)
- **E Drive**: ~6GB (models and cache)

## How to Run

### Option 1: Batch File (Windows CMD)
```cmd
cd C:\Users\ASAA\Documents\vanimitra
start_app.bat
```

### Option 2: PowerShell Script
```powershell
cd C:\Users\ASAA\Documents\vanimitra
.\start_app.ps1
```

### Option 3: Manual
```cmd
set HF_HOME=E:\VaaniMitraData\cache
set HF_HUB_CACHE=E:\VaaniMitraData\cache
set TRANSFORMERS_CACHE=E:\VaaniMitraData\cache
python app.py
```

## First Run Notes
- First startup will download ~1GB of AI models to E drive
- This may take 10-20 minutes depending on internet speed
- Subsequent runs will be much faster (models cached)

## Troubleshooting

### E Drive Not Available
If you don't have an E drive, edit the scripts to use a different drive:
1. Open `start_app.bat` or `start_app.ps1`
2. Change `E:\VaaniMitraData\` to your preferred path (e.g., `D:\VaaniMitraData\`)
3. Update `indictrans2_service.py` cache_dir paths accordingly

### Permission Issues
Ensure you have write permissions to the E drive. If not, run the scripts as Administrator or choose a different location.

### Cleanup
To remove all VaaniMitra data from E drive:
```cmd
Remove-Item -Recurse -Force E:\VaaniMitraData
```

## Status
✅ E drive configured
✅ Startup scripts created
✅ App code updated
✅ README updated
⏳ Models downloading (first run)