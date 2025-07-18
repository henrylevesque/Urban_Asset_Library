#!/usr/bin/env python3
"""
Urban Asset Library - Automated README Generator

This script automatically generates README.md files for all asset folders
that contain 3D files (.stl, .stp) and preview images (.png).

Author: Henry Levesque
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

def clean_filename(filename: str) -> str:
    """Clean filename for display (remove extensions, improve formatting)"""
    name = Path(filename).stem
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    # Capitalize first letter of each word
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def get_asset_files(folder_path: Path) -> Dict[str, List[str]]:
    """Get all asset files in a folder, organized by type"""
    files = {
        'stl': [],
        'stp': [],
        'png': [],
        'other': []
    }
    
    if not folder_path.exists():
        return files
    
    for file in folder_path.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            if ext == '.stl':
                files['stl'].append(file.name)
            elif ext == '.stp':
                files['stp'].append(file.name)
            elif ext == '.png':
                files['png'].append(file.name)
            elif ext in ['.obj', '.3mf', '.step', '.iges']:
                files['other'].append(file.name)
    
    return files

def generate_readme_content(folder_name: str, files: Dict[str, List[str]], 
                          relative_path: str = "") -> str:
    """Generate README content for an asset folder"""
    
    # Create a clean asset name
    asset_name = clean_filename(folder_name)
    
    # Start building the README content
    content = f"# {asset_name}\n\n"
    
    # Add description based on folder structure
    description = get_asset_description(folder_name, relative_path)
    content += f"{description}\n\n"
    
    # Add preview images
    if files['png']:
        content += "## Preview\n\n"
        primary_image = files['png'][0]
        content += f"![{asset_name}]({primary_image})\n\n"
        
        # Add additional images if available
        if len(files['png']) > 1:
            content += "*Additional views:*\n"
            for img in files['png'][1:]:
                img_name = clean_filename(img)
                content += f"![{img_name}]({img})\n"
            content += "\n"
    
    # Add specifications
    content += "## Specifications\n\n"
    content += "- **Scale**: 1:48 (HO Scale)\n"
    content += "- **Material**: Designed for PLA/PETG 3D printing\n"
    content += "- **Print Time**: Varies by complexity\n"
    content += "- **Support Required**: Minimal (model optimized for printing)\n\n"
    
    # Add files table
    if files['stl'] or files['stp'] or files['png']:
        content += "## Files Available\n\n"
        content += "| File | Format | Description |\n"
        content += "|------|---------|-------------|\n"
        
        # Add STL files
        for stl_file in files['stl']:
            content += f"| `{stl_file}` | STL | 3D printable mesh file |\n"
        
        # Add STP files
        for stp_file in files['stp']:
            content += f"| `{stp_file}` | STP | CAD file for editing |\n"
        
        # Add PNG files
        for png_file in files['png']:
            content += f"| `{png_file}` | PNG | Preview image |\n"
        
        # Add other files
        for other_file in files['other']:
            ext = Path(other_file).suffix.upper()[1:]
            content += f"| `{other_file}` | {ext} | 3D model file |\n"
        
        content += "\n"
    
    # Add usage section
    content += "## Usage\n\n"
    content += "### 3D Printing\n"
    content += "- **Layer Height**: 0.2mm (0.15mm for fine details)\n"
    content += "- **Infill**: 15-20% (adjust based on use case)\n"
    content += "- **Print Speed**: 50-60 mm/s\n"
    content += "- **Supports**: Usually not required\n\n"
    
    # Add applications
    applications = get_asset_applications(folder_name, relative_path)
    content += "### Applications\n"
    for app in applications:
        content += f"- {app}\n"
    content += "\n"
    
    # Add download section
    if files['stl'] or files['stp']:
        content += "## Download\n\n"
        for stl_file in files['stl']:
            content += f"- [Download STL file]({stl_file})\n"
        for stp_file in files['stp']:
            content += f"- [Download STP file]({stp_file})\n"
        content += "\n"
    
    # Add attribution
    content += "## Attribution\n\n"
    content += "When using this asset, please cite:\n"
    content += "```\n"
    content += "Author: Henry Levesque\n"
    content += f"Source: Urban Asset Library - {asset_name}\n"
    content += "URL: https://github.com/hleve/Urban_Asset_Library\n"
    content += "```\n\n"
    
    # Add related assets
    content += "## Related Assets\n\n"
    content += get_related_assets_links(relative_path)
    
    # Add footer
    content += "---\n\n"
    content += "*Part of the [Urban Asset Library](../../../) - Open source urban assets for simulation and 3D printing*"
    
    return content

def get_asset_description(folder_name: str, relative_path: str) -> str:
    """Generate description based on folder name and path"""
    descriptions = {
        'bollard': "Bollards for controlling vehicle access while maintaining pedestrian flow.",
        'decorative bollard': "A decorative bollard for urban environments, perfect for controlling vehicle access while maintaining aesthetic appeal.",
        'plain bollard': "A simple, functional bollard for basic vehicle access control.",
        'stop sign': "Standard traffic stop sign for intersection control.",
        'yield sign': "Standard yield sign for traffic flow management.",
        'warning sign': "Warning signage for various traffic and safety alerts.",
        'sign post': "Support posts for mounting various traffic and informational signs.",
        'curb': "Concrete curbing for road edge definition and water management.",
        'sidewalk': "Pedestrian walkway infrastructure in various textures and styles.",
        'road': "Roadway sections for creating street networks in urban models.",
        'utility pole': "Infrastructure support poles for power lines and utilities.",
        'storm drain': "Drainage infrastructure for stormwater management.",
        'bus stop': "Public transit infrastructure for passenger boarding areas.",
        'dumpster': "Waste management containers in various sizes.",
        'barrier': "Safety and construction barriers for crowd and traffic control.",
        'lane marking': "Road surface markings for traffic lane definition.",
    }
    
    folder_lower = folder_name.lower()
    for key, desc in descriptions.items():
        if key in folder_lower:
            return desc
    
    # Default description
    return f"Urban asset for {clean_filename(folder_name).lower()} applications in city planning and simulation."

def get_asset_applications(folder_name: str, relative_path: str) -> List[str]:
    """Get relevant applications for the asset type"""
    base_apps = [
        "Urban planning models",
        "Architectural visualizations", 
        "City planning presentations",
        "3D printed scale models"
    ]
    
    folder_lower = folder_name.lower()
    
    if 'sign' in folder_lower:
        return base_apps + [
            "Traffic flow simulations",
            "Road safety analysis",
            "Driver training scenarios"
        ]
    elif 'road' in folder_lower or 'street' in folder_lower:
        return base_apps + [
            "Traffic simulation research",
            "Transportation planning",
            "Infrastructure modeling"
        ]
    elif 'transit' in folder_lower or 'bus' in folder_lower:
        return base_apps + [
            "Public transit planning",
            "Passenger flow analysis",
            "Transit system design"
        ]
    else:
        return base_apps + [
            "Digital twin development",
            "Smart city research"
        ]

def get_related_assets_links(relative_path: str) -> str:
    """Generate links to related assets based on current path"""
    path_parts = relative_path.split('/')
    
    if len(path_parts) >= 2:
        category = path_parts[0]
        links = f"- [Other {category} Assets](../../)\n"
        links += "- [All Urban Assets](../../../)\n"
    else:
        links = "- [All Urban Assets](../)\n"
    
    return links

def should_create_readme(folder_path: Path) -> bool:
    """Check if folder should have a README (contains 3D assets)"""
    files = get_asset_files(folder_path)
    return len(files['stl']) > 0 or len(files['stp']) > 0 or len(files['other']) > 0

def process_folder(folder_path: Path, base_path: Path, force_overwrite: bool = False):
    """Process a single folder and generate README if needed"""
    if not should_create_readme(folder_path):
        return
    
    readme_path = folder_path / "README.md"
    
    # Skip if README exists and not forcing overwrite
    if readme_path.exists() and not force_overwrite:
        print(f"⏭️  Skipping {folder_path.name} (README already exists)")
        return
    
    # Get relative path for links
    relative_path = str(folder_path.relative_to(base_path))
    
    # Get asset files
    files = get_asset_files(folder_path)
    
    # Generate README content
    content = generate_readme_content(folder_path.name, files, relative_path)
    
    # Write README file
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created README for {folder_path.name}")
    except Exception as e:
        print(f"❌ Error creating README for {folder_path.name}: {e}")

def main():
    """Main function to process all folders"""
    # Get the script directory (should be repository root)
    base_path = Path(__file__).parent
    
    print("🏗️  Urban Asset Library - README Generator")
    print("=" * 50)
    
    # Ask user for preferences
    force_overwrite = input("\n🔄 Overwrite existing README files? (y/N): ").lower().startswith('y')
    
    # Folders to process (exclude certain directories)
    exclude_dirs = {'.git', '__pycache__', 'working_files', 'asset_dictionaries', '.vscode'}
    
    readme_count = 0
    
    # Process all directories recursively
    for root, dirs, files in os.walk(base_path):
        # Remove excluded directories from dirs list
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        current_path = Path(root)
        
        # Skip the root directory
        if current_path == base_path:
            continue
        
        # Process this directory
        process_folder(current_path, base_path, force_overwrite)
        readme_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎉 Processing complete! Processed {readme_count} folders.")
    print("\n📝 Next steps:")
    print("1. Review the generated README files")
    print("2. Commit changes to your repository")
    print("3. Your assets now have individual documentation!")

if __name__ == "__main__":
    main()
