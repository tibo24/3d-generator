A small Python project to create a 3d model of a stamp from a drawing. Option to resize and move drawing imported onto canvas.

**Requirements**
- **Python:** 3.10+ recommended.
- **Dependencies:** listed in `requirements.txt` — install with pip as shown below.

**Quick Start (Windows)**
- Create and activate a virtual environment, install dependencies, then run the app:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Usage**
- Running `app.py` launches the application. The program opens an interactive canvas window (using the libraries in `requirements.txt`) where the project's drawing/3D functionality can be explored.

**Development Notes**
- Use a virtual environment to avoid polluting your global Python installation.
- The project relies on libraries such as `numpy`, `pyglet`, `trimesh`, and `pillow` (see `requirements.txt`).s