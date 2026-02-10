**Development of a Set of Software Components for a Production System of Badges and Logos of BrSTU**  

## 1. PROJECTION (Requirements Gathering and Analysis)

We, as systems analysts, have collected (or plan to collect) requirements from the "customer" — the head of the laboratory / lab engineer.

### Key Questions Asked / Clarified:
- **System Goal**: Automate the preparation and launch of production for badges, name tags, and souvenirs featuring BrSTU branding.
- **Types of Products**:
  - Pin-back buttons (закатные значки) Ø 25–58 mm
  - Acrylic / plastic name badges
  - Wooden / metal items with logo engraving
  - Stickers / decals with UV printing
- **Customization**: Yes — support for personalization (student's full name, group number, employee's position)
- **Typical Order Workflow**:
  1. User (operator / student) selects product type and logo template
  2. Enters personalization data (if required)
  3. The program generates a ready file (SVG / DXF / PDF)
  4. The file is automatically sent to the machine (via shared folder / direct command)
  5. Operator confirms start on the machine
- **Laboratory Equipment Inventory** (after visit):
  - Laser engraver / cutter (e.g., GCC LaserPro / Chinese 6040) → supports .dxf, .svg, .plt
  - UV printer (Roland / Mimaki) → raster files + RIP software
  - Press for pin-back buttons (manual / semi-automatic)
  - Vinyl cutter plotter (if available)
- **Formats and Connectivity**:
  - Main exchange format: SVG (vector, easily scalable)
  - File transfer: via shared network folder (\\lab-pc\shared\jobs) or USB drive
  - API / direct control: not discovered yet; file-based transfer + manual start is used

## 2. Technology Stack and Architecture

Goal — a simple, extensible solution that will not die after the course ends.

### Technology Stack
- **Language**: Python 3.10+
- **Graphics Generation**:
  - `cairosvg` — rendering SVG to raster
  - `svgwrite` — programmatic SVG creation/editing
  - `Pillow` — raster image processing
- **User Interface**:
  - Desktop: `PyQt6` (or `tkinter` for minimal prototype)
  - Alternative: web interface on `Streamlit` (faster deployment in the lab)
- **Data Storage**:
  - SQLite + SQLAlchemy — database for templates and batches
  - Folder `templates/` — vector logo files of BrSTU (.svg)
- **Configuration**: YAML files for calibration (margins, laser power per material)

### Extensibility
- New logo → simply add .svg file to `templates/logos/`
- New product type → add entry to `config/products.yaml`
- New material → add calibration parameters to `config/materials.yaml`

## 3. Implementation Stages (Current Progress)

1. **Information Gathering** — partially completed (lab visit, equipment photos)
2. **Layout Generation Prototype** — in progress
   - Script overlays BrSTU logo onto pin-back button template
   - Personalization text support
3. **Selection & Launch Interface** — prototype on Streamlit
4. **File Transfer to Machine** — implemented via copy to shared folder
5. **Testing** — scheduled for March 2026 (test batch of 10 badges)

## 4. Plan in Case of Incomplete Project

If not everything is finished by the deadline:

- **What Already Works**:
  - SVG generation with logo and text
  - Simple GUI for template selection
  - Automatic saving to jobs/ folder
- **What Was Not Completed**:
  - Full integration with UV printer (RIP processing)
  - Job queue and status monitoring
  - Automatic check for BrSTU brand book compliance
- **Recommendations for Future Developers**:
  1. Add G-code support for CNC/laser machines
  2. Implement web-based order submission interface (Flask + SQLite)
  3. Add logging and material consumption tracking

## 5. Results and Update Deployment Method

- **Repository**: reports/Potapchuk/15/
- **Main Files**:
  - `src/main.py` — entry point
  - `src/templates/` — BrSTU logos (.svg)
  - `src/config/` — YAML configuration files
  - `rep/` — this documentation + screenshots

**How to Update the System** (for lab engineer / "system keeper"):

1. Download new logo in .svg → place it in `templates/logos/`
2. For a new product type — edit `config/products.yaml`
3. Restart the program (or press "Refresh Templates" button in the interface)
