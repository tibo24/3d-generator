import subprocess
import tempfile
import os
from PIL import Image, ImageGrab

def canvas_to_png(canvas, output_path):
    # Get canvas position on screen
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = x + canvas.winfo_width()
    h = y + canvas.winfo_height()

    # Grab the canvas area
    img = ImageGrab.grab((x, y, w, h))
    img.save(output_path)

def canvas_to_svg(canvas, potrace_path="potrace.exe"):
    # 1. Save canvas as PNG
    fd_png, temp_png = tempfile.mkstemp(suffix=".png")
    os.close(fd_png)
    canvas_to_png(canvas, temp_png)

    # 2. Convert PNG → PBM
    fd_pbm, temp_pbm = tempfile.mkstemp(suffix=".pbm")
    os.close(fd_pbm)

    img = Image.open(temp_png).convert("L")
    bw = img.point(lambda x: 0 if x < 128 else 255, "1")
    bw.save(temp_pbm)

    # 3. Run Potrace
    fd_svg, temp_svg = tempfile.mkstemp(suffix=".svg")
    os.close(fd_svg)

    subprocess.run([
        potrace_path,
        temp_pbm,
        "-s",
        "-o", temp_svg
    ], check=True)

    # 4. Read SVG
    with open(temp_svg, "r") as f:
        svg_data = f.read()

    # Cleanup
    os.remove(temp_png)
    os.remove(temp_pbm)
    os.remove(temp_svg)

    return svg_data
