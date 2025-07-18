# Scripts

This directory contains automation scripts for the Urban Asset Library.

## Available Scripts

### `generate_asset_docs.py`
Automatically generates individual README.md files for all asset folders.

**Usage:**
```bash
python scripts/generate_asset_docs.py
```

**Features:**
- Scans all folders for 3D assets (STL, STP files)
- Automatically detects and includes PNG preview images
- Generates consistent, professional documentation
- Creates navigation links between related assets
- Includes proper attribution and usage instructions

**Requirements:**
- Python 3.6+
- No additional dependencies required

## Running Scripts

From the repository root:
```bash
# Generate asset documentation
python scripts/generate_asset_docs.py

# Future scripts can be added here
```

## Adding New Scripts

When adding new automation scripts:
1. Place them in this `scripts/` directory
2. Update this README with usage instructions
3. Follow the existing code style and documentation patterns
4. Test thoroughly before committing
