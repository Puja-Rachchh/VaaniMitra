# VaaniMitra
Interactive Multilingual Tutor for Indian Regional Languages

## Storage Configuration

VaaniMitra uses AI models that require significant disk space. By default, models are stored on your E drive to save space on C drive.

### Directory Structure
```
E:\VaaniMitraData\
├── models\          # AI model files (~1GB)
└── cache\           # HuggingFace cache (~5GB)
```

### Running the App

**Option 1: Batch file (Recommended)**
```cmd
start_app.bat
```

**Option 2: PowerShell script**
```powershell
.\start_app.ps1
```

**Option 3: Manual setup**
```cmd
set HF_HOME=E:\VaaniMitraData\cache
set HF_HUB_CACHE=E:\VaaniMitraData\cache
set TRANSFORMERS_CACHE=E:\VaaniMitraData\cache
python app.py
```

### Space Requirements
- **Models**: ~1GB (IndicTrans2 translation models)
- **Cache**: ~5GB (HuggingFace download cache)
- **Virtual Environment**: ~1.5GB (Python packages)
- **Total**: ~7.5GB

### Troubleshooting
If you don't have an E drive, you can modify the paths in:
- `start_app.bat`
- `start_app.ps1`
- `indictrans2_service.py` (cache_dir parameters)
