# Urban Asset Library

![GitHub Stars](https://img.shields.io/github/stars/hleve/Urban_Asset_Library?style=social)
![GitHub Forks](https://img.shields.io/github/forks/hleve/Urban_Asset_Library?style=social)
![License](https://img.shields.io/github/license/hleve/Urban_Asset_Library)
![GitHub Issues](https://img.shields.io/github/issues/hleve/Urban_Asset_Library)

Welcome to the **Open-Source Urban Asset Library**! To imagine future urban environments, we must first understand current urban environments, which means understanding what exists in current environments. This repository is a comprehensive collection of urban assets designed for creating urban digital twins for simulation research, urban planning, and smart city development.

🔗 **Also available on [Printables.com](https://www.printables.com/@HenryLevesque/collections/1560825)**

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Asset Categories](#asset-categories)
- [File Formats](#file-formats)
- [Usage Examples](#usage-examples)
- [Installation](#installation)
- [3D Printing Guide](#3d-printing-guide)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

## ✨ Features

- **Comprehensive Asset Collection**: Street infrastructure, signage, transit elements, and more
- **Multiple File Formats**: STL, STP, PNG files for various applications
- **Scalable Models**: Designed at 1:48 scale but can be scaled for your needs
- **Research-Ready**: Perfect for urban simulation, digital twins, and planning research
- **3D Printable**: All models optimized for 3D printing
- **Open Source**: Free to use with proper attribution

## 🚀 Quick Start

### Download Individual Assets
1. Navigate to the desired asset folder
2. Download the file you need (.stl, .stp, or .png)
3. Use in your project with proper attribution

### Clone the Entire Library
```bash
git clone https://github.com/hleve/Urban_Asset_Library.git
cd Urban_Asset_Library
```

## 🏙️ Asset Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **[Street](Street/)** | Road infrastructure and elements | Roads, curbs, sidewalks, bollards, utility poles |
| **[Signage](Signage/)** | Traffic and warning signs | Stop signs, yield signs, warning signs, sign posts |
| **[Transit](Transit/)** | Public transportation assets | Bus stops, transit shelters |
| **[MISC](MISC/)** | Miscellaneous urban elements | Dumpsters, barriers, fencing |
| **[Unsorted](Unsorted/)** | New or uncategorized assets | Furniture, planters, decorative elements |

📖 **[View Complete Asset Catalog](Table_of_Contents.md)**

## 📁 File Formats

- **`.stl`** - 3D printable files, mesh format
- **`.stp`** - CAD files, parametric format for editing
- **`.png`** - Reference images and previews

## 💡 Usage Examples

### Urban Simulation Research
```python
# Example: Load assets for digital twin simulation
import trimesh

# Load a street asset
street = trimesh.load('Street/Road/Single Lane Road/single_lane_road.stl')
sidewalk = trimesh.load('Street/Sidewalk/Simple Sidewalk/simple_sidewalk.stl')

# Combine for simulation environment
scene = trimesh.Scene([street, sidewalk])
```

### 3D Printing for Physical Models
1. Choose your desired scale (default: 1:48)
2. Download the `.stl` file
3. Import into your slicer software
4. Print with recommended settings (see [3D Printing Guide](#3d-printing-guide))

### CAD Integration
1. Download the `.stp` file for parametric editing
2. Import into your CAD software (SolidWorks, Fusion 360, etc.)
3. Modify as needed for your specific use case

## 🔧 Installation

### Requirements
- No special software required for basic usage
- For 3D printing: Slicer software (PrusaSlicer, Cura, etc.)
- For CAD editing: CAD software supporting STP format

### Optional: Python Environment for Asset Management
```bash
# Create virtual environment
python -m venv urban_assets_env
source urban_assets_env/bin/activate  # On Windows: urban_assets_env\Scripts\activate

# Install dependencies for asset catalog generation
pip install fpdf pillow pandas openpyxl
```

## 🖨️ 3D Printing Guide

### Recommended Settings
- **Scale**: 1:48 (or adjust as needed)
- **Layer Height**: 0.2mm
- **Infill**: 15-20%
- **Supports**: Usually not required (models are print-friendly)

### Print Quality Tips
- **Street Assets**: Use higher infill (20-25%) for durability
- **Signage**: Lower infill (10-15%) is sufficient
- **Fine Details**: Consider 0.15mm layer height for small elements

### Post-Processing
- Light sanding for smooth surfaces
- Paint with acrylics for realistic appearance
- Clear coat for durability in outdoor displays

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute
1. **Fork** the repository
2. **Create** a new branch for your asset
3. **Add** your asset files (STL, STP, PNG)
4. **Update** documentation
5. **Submit** a pull request

### Asset Guidelines
- Models should be manifold and printable
- Include both STL and STP formats if possible
- Add a reference image (PNG)
- Follow the existing folder structure
- Ensure proper scale (1:48 recommended)

### Asset Requests
Have an idea for a new asset? [Open an issue](https://github.com/hleve/Urban_Asset_Library/issues) with the "asset request" label.

## 📄 Citation

If you use assets from this library in your research or projects, please cite:

```bibtex
@software{levesque2024urban,
  author = {Levesque, Henry},
  title = {Urban Asset Library},
  version = {1.0.0},
  year = {2024},
  url = {https://github.com/hleve/Urban_Asset_Library},
  doi = {10.5281/zenodo.14647594}
}
```

**Or use the citation information from [CITATION.cff](CITATION.cff)**

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Attribution Required
When using these assets, you must provide proper attribution. Include:
- Author: Henry Levesque
- Source: Urban Asset Library
- URL: https://github.com/hleve/Urban_Asset_Library

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/hleve/Urban_Asset_Library/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hleve/Urban_Asset_Library/discussions)
- **Email**: Contact via GitHub profile

## 🙏 Acknowledgments

Special thanks to all contributors and the open-source community for making this project possible.

---

**⭐ Star this repository if you find it useful!**

Thank you for using the Open Source Urban Asset Library!
