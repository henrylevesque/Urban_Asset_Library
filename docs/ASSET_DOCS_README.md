# Asset Documentation Generator

This script automatically generates individual README.md files for all your urban assets.

## Quick Start

1. **Run the script:**
   ```bash
   python scripts/generate_asset_docs.py
   ```

2. **Follow the prompts:**
   - Choose whether to overwrite existing README files
   - The script will process all folders containing 3D assets

3. **Review the results:**
   - Each asset folder will get a comprehensive README.md
   - Includes images, specifications, and download links
   - Provides consistent formatting across all assets

## What Gets Generated

For each asset folder, the script creates:

- **Asset title and description**
- **Preview images** (automatically detects PNG files)
- **Specifications** (scale, materials, print settings)
- **File inventory** (STL, STP, PNG files)
- **Usage instructions** (3D printing settings, applications)
- **Download links** (direct links to files)
- **Attribution information**
- **Related assets** (navigation links)

## Features

- ✅ **Automatic detection** of 3D files (.stl, .stp, .obj, etc.)
- ✅ **Smart descriptions** based on folder names and categories
- ✅ **Image integration** with all PNG files in folders
- ✅ **Consistent formatting** across all documentation
- ✅ **Navigation links** between related assets
- ✅ **3D printing guidance** for each asset
- ✅ **Professional presentation** with proper attribution

## Example Output

Each README includes sections like:
- Preview images
- Technical specifications
- Available file formats
- 3D printing settings
- Usage applications
- Download links
- Attribution requirements

## Customization

You can modify the script to:
- Change default descriptions
- Adjust 3D printing recommendations
- Add custom file types
- Modify the template structure

## Next Steps

After running the script:
1. Review generated README files
2. Commit changes to your repository
3. Your asset library now has comprehensive documentation!
