import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.canvas import canvas_to_svg
from src.trim import create_stempel
import tempfile
from pathlib import Path

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Maak stempel")
        self.root.iconbitmap('assets/stempel.ico')

        self.canvas = tk.Canvas(root, width=800, height=800, bg="lightgray")
        self.canvas.create_oval(100, 100, 700, 700, outline="black", width=10, fill="", tags="border")
        self.canvas.pack()
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)
        self.keep_border = tk.BooleanVar()
        self.height_slider = tk.Scale(self.frame, orient="horizontal")
        self.height_slider.set(50)
        self.border_chk = tk.Checkbutton(self.frame, text="Rand", onvalue=True, offvalue=False, variable=self.keep_border)
        self.upload_btn = tk.Button(self.frame, text="Upload afbeelding", command=self.upload_image)
        self.preview_btn = tk.Button(self.frame, text="Voorbeeld", command=self.preview_model)
        self.save_btn = tk.Button(self.frame, text="Opslaan", command=self.save_model)
        self.height_slider.pack(side=tk.LEFT, padx=10)
        self.border_chk.pack(side=tk.LEFT, padx=10)
        self.upload_btn.pack(side=tk.LEFT, padx=10)
        self.preview_btn.pack(side=tk.LEFT, padx=10)
        self.save_btn.pack(side=tk.LEFT, padx=10)   
        
        self.img = None
        self.tk_img = None
        self.img_id = None
        self.scale = 2.0

        # Drag state
        self.drag_data = {"x": 0, "y": 0}

    def upload_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if not path:
            return

        up_img = Image.open(path)
        
        # Canvas size
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        # Image size
        iw, ih = up_img.size
        
        scale = min(cw / iw, ch / ih)
        resized = up_img.resize((int(iw * scale), int(ih * scale)), Image.LANCZOS)
        self.img = resized
        self.scale = 1.0
        self.render_image()

        # Bind interactions
        self.canvas.tag_bind(self.img_id, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.img_id, "<B1-Motion>", self.drag)
        self.canvas.bind("<MouseWheel>", self.resize)
        self.canvas.tag_raise('border')

    def create_model(self):
        print(self.height_slider.get())
        if not self.keep_border.get():
            self.canvas.delete("border")
            self.canvas.update_idletasks() 
            svg = canvas_to_svg(self.canvas)
            self.canvas.create_oval(100, 100, 700, 700, outline="black", width=10, fill="", tags="border")
            self.canvas.update_idletasks() 
        else:
            svg = canvas_to_svg(self.canvas)

        with tempfile.TemporaryDirectory() as tmpdir:
            svg_path = Path(tmpdir) / "image.svg"
            svg_path.write_text(svg, encoding="utf-8")
            self.model = create_stempel(svg_path, self.height_slider.get())

    def preview_model(self):
        self.create_model()
        self.model.show()

    def save_model(self):
        self.create_model()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl")]
        )
        if not file_path:
            return
        
        self.model.export(file_path)
        
    def save_canvas_to_svg(self):
        self.canvas.delete("border")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")]
        )
        if not file_path:
            return

        svg = canvas_to_svg(self.canvas)
        with open(file_path, "w") as f:
            f.write(svg)

        print("SVG saved:", file_path)

    def render_image(self):
        # Resize image according to scale
        w, h = self.img.size
        resized = self.img.resize((int(w * self.scale), int(h * self.scale)))
        self.tk_img = ImageTk.PhotoImage(resized)

        if self.img_id is None:
            self.img_id = self.canvas.create_image(300, 250, image=self.tk_img)
        else:
            self.canvas.itemconfig(self.img_id, image=self.tk_img)

    # --- Dragging ---
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.img_id, dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    # --- Resizing ---
    def resize(self, event):
        if event.delta > 0:
            self.scale *= 1.1
        else:
            self.scale *= 0.9

        self.scale = max(0.1, min(self.scale, 5.0))  # clamp
        self.render_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
    
