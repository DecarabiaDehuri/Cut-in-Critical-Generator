import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class PortraitApp:
    def __init__(self, master):
        self.master = master
        master.title("Cut-in Critical Generator")

        # Configuration
        self.frame_positions = {
            5: 179, 6: 147, 7: 131, 8: 99, 9: 100, 10: 101,
            11: 102, 12: 103, 13: 104, 14: 105, 15: 103,
            16: 101, 17: 99, 18: 79, 19: 59
        }
        self.default_y = 115
        self.template_dir = "Template"
        self.preview_frame = 10

        # GUI Elements
        self.create_widgets()
        self.disable_controls()

    def create_widgets(self):
        # Portrait Selection
        self.btn_select = tk.Button(
            self.master,
            text="Select Portrait",
            command=self.select_portrait
        )
        self.btn_select.pack(pady=5)

        # Offset Controls
        self.x_offset = tk.IntVar()
        self.y_offset = tk.IntVar()

        tk.Label(self.master, text="X Offset").pack()
        self.scl_x = tk.Scale(
            self.master,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.x_offset,
            command=self.update_preview
        )
        self.scl_x.pack()

        tk.Label(self.master, text="Y Offset").pack()
        self.scl_y = tk.Scale(
            self.master,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.y_offset,
            command=self.update_preview
        )
        self.scl_y.pack()

        # Character Name
        tk.Label(self.master, text="Character Name").pack()
        self.ent_name = tk.Entry(self.master, width=30)
        self.ent_name.pack(pady=5)

        # Generate Button
        self.btn_generate = tk.Button(
            self.master,
            text="Generate",
            command=self.generate_output
        )
        self.btn_generate.pack(pady=5)

        # Preview
        self.lbl_preview = tk.Label(self.master)
        self.lbl_preview.pack(pady=10)

    def disable_controls(self):
        self.scl_x.config(state=tk.DISABLED)
        self.scl_y.config(state=tk.DISABLED)
        self.btn_generate.config(state=tk.DISABLED)

    def enable_controls(self):
        self.scl_x.config(state=tk.NORMAL)
        self.scl_y.config(state=tk.NORMAL)
        self.btn_generate.config(state=tk.NORMAL)

    def select_portrait(self):
        file_path = filedialog.askopenfilename(
            title="Select Portrait Image",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                self.portrait = Image.open(file_path).convert("RGBA")
                self.enable_controls()
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def update_preview(self, *args):
        if not hasattr(self, 'portrait'):
            return

        try:
            frame_path = os.path.join(self.template_dir, f"{self.preview_frame}.png")
            base_img = Image.open(frame_path).convert("RGBA")
            applied_img = self.apply_portrait(base_img, self.preview_frame)
            
            preview_img = ImageTk.PhotoImage(applied_img)
            self.lbl_preview.config(image=preview_img)
            self.lbl_preview.image = preview_img
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed:\n{e}")

    def apply_portrait(self, base_image, frame_number):
        base_x = self.frame_positions.get(frame_number)
        if base_x is None:
            return base_image

        img = base_image.copy()
        x = base_x + self.x_offset.get()
        y = self.default_y + self.y_offset.get()
        portrait = self.portrait

        # Calculate overlap area
        pw, ph = portrait.size
        iw, ih = img.size

        overlap_left = max(x, 0)
        overlap_top = max(y, 0)
        overlap_right = min(x + pw, iw)
        overlap_bottom = min(y + ph, ih)

        if overlap_left >= overlap_right or overlap_top >= overlap_bottom:
            return img

        # Get template region and create mask
        template_region = img.crop((overlap_left, overlap_top, overlap_right, overlap_bottom))
        mask = template_region.getchannel("A").point(lambda p: 255 if p == 255 else 0)

        # Crop portrait to overlap area
        portrait_left = max(0 - x, 0)
        portrait_top = max(0 - y, 0)
        portrait_crop = portrait.crop((
            portrait_left,
            portrait_top,
            portrait_left + (overlap_right - overlap_left),
            portrait_top + (overlap_bottom - overlap_top)
        )).convert("RGBA")

        # Composite portrait over template region
        composite_region = Image.alpha_composite(template_region, portrait_crop)

        # Paste back only on original opaque areas
        img.paste(composite_region, (overlap_left, overlap_top), mask=mask)

        return img

    def generate_output(self):
        char_name = self.ent_name.get().strip()
        if not char_name:
            messagebox.showerror("Error", "Please enter a character name")
            return

        output_dir = char_name
        os.makedirs(output_dir, exist_ok=True)

        try:
            for frame_num in range(1, 21):
                frame_path = os.path.join(self.template_dir, f"{frame_num}.png")
                base_img = Image.open(frame_path).convert("RGBA")
                
                if frame_num in self.frame_positions:
                    final_img = self.apply_portrait(base_img, frame_num)
                else:
                    final_img = base_img
                
                final_img.save(os.path.join(output_dir, f"{frame_num}.png"))

            messagebox.showinfo("Success", f"Output generated in:\n{os.path.abspath(output_dir)}")
        except Exception as e:
            messagebox.showerror("Error", f"Generation failed:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PortraitApp(root)
    root.mainloop()
