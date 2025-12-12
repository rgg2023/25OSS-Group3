import platform
import ctypes
import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
from filters.mosaic import apply_mosaic_to_faces
from filters.grayscale import apply_grayscale
from filters.cartoon import apply_cartoon
from filters.sketch import apply_sketch
from filters.invert import apply_invert
from filters.blur import apply_blur
from filters.edge_detection import apply_edge_detection
from filters.sepia import apply_sepia
from filters.brightness import apply_brightness
from filters.saturation import apply_saturation
from filters.hdr_effect import apply_hdr_effect
from filters.vignette import apply_vignette
from filters.portrait_mode import apply_portrait_mode
from filters.remove_person import apply_remove_person
from filters.sticker import apply_sticker
from PIL import Image, ImageTk
import numpy as np
import os

# DPI 설정 (Windows)
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter App")
        self.root.geometry("400x800")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # 이미지 관련 변수
        self.cv_images = []
        self.original_images = []
        self.original_file_paths = []
        self.current_index = 0
        self.filters_applied = []

        self.init_gui()

    def init_gui(self):
        # 상단 타이틀
        title_label = ctk.CTkLabel(self.root, text="Photo Filter App", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=15)

        # Open / Save 버튼
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.pack(pady=5, padx=10, fill="x")

        btn_open = ctk.CTkButton(button_frame_top, text="Open Images", command=self.open_images,
                                 fg_color="#007AFF", hover_color="#0051a8", width=150)
        btn_open.pack(side="left", padx=10)

        btn_save = ctk.CTkButton(button_frame_top, text="Save All", command=self.save_all_images,
                                 fg_color="#34C759", hover_color="#28a745", width=150)
        btn_save.pack(side="right", padx=10)

        # 이미지 캔버스
        self.canvas_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.canvas_frame.pack(pady=10, padx=15, fill="both", expand=True)
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#f0f0f0", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 필터 라벨
        self.filter_label = ctk.CTkLabel(self.root, text="Current Filter: None", font=("Helvetica", 16, "bold"))
        self.filter_label.pack(pady=5)

        # 하단 필터 버튼 스크롤 프레임 (모바일 느낌)
        self.button_frame_scroll = ctk.CTkScrollableFrame(self.root, label_text="Filters",
                                                          label_text_color="#007AFF",
                                                          fg_color="#2C3E50",
                                                          orientation="horizontal", height=100)
        self.button_frame_scroll.pack(pady=10, padx=10, fill="x")

        # 필터 버튼 목록
        filters = [
            ("Mosaic", self.apply_mosaic_filter), ("Grayscale", self.apply_grayscale_filter),
            ("Cartoon", self.apply_cartoon_filter), ("Sketch", self.apply_sketch_filter),
            ("Invert", self.apply_invert_filter), ("Blur", self.apply_blur_filter),
            ("Edge", self.apply_edge_filter), ("Sepia", self.apply_sepia_filter),
            ("Brightness", self.apply_brightness_filter), ("Saturation", self.apply_saturation_filter),
            ("HDR", self.apply_hdr_filter), ("Vignette", self.apply_vignette_filter),
            ("Portrait Mode", self.apply_portrait_mode_filter),
            ("Remove Person", self.apply_remove_person_filter), ("Sticker", self.apply_sticker_filter),
        ]

        for i, (text, command) in enumerate(filters):
            btn = ctk.CTkButton(self.button_frame_scroll, text=text, command=command,
                                width=100, height=40, corner_radius=15, fg_color="#34495E")
            btn.grid(row=0, column=i, padx=8, pady=10)

    # ================= 이미지 로딩 =================
    def open_images(self):
        file_paths = filedialog.askopenfilenames(initialdir="../test_img",
                                                 filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if not file_paths:
            return
        self.cv_images.clear()
        self.original_images.clear()
        self.original_file_paths.clear()
        self.filters_applied.clear()

        for path in file_paths:
            data = np.fromfile(path, dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            self.original_images.append(image)
            self.cv_images.append(image.copy())
            self.original_file_paths.append(path)
            self.filters_applied.append("None")

        self.current_index = 0
        self.update_filter_label()
        self.display_image()

    # ================= 필터 적용 =================
    def apply_filter(self, func, name):
        if not self.cv_images:
            return
        if self.filters_applied[self.current_index] == name:
            self.cv_images[self.current_index] = self.original_images[self.current_index].copy()
            self.filters_applied[self.current_index] = "None"
        else:
            self.cv_images[self.current_index] = func(self.original_images[self.current_index].copy())
            self.filters_applied[self.current_index] = name
        self.update_filter_label()
        self.display_image()

    def save_all_images(self):
        if not self.cv_images:
            return
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        for idx, img in enumerate(self.cv_images):
            original_name = os.path.splitext(os.path.basename(self.original_file_paths[idx]))[0]
            filter_name = self.filters_applied[idx] if self.filters_applied[idx] != "None" else "original"
            save_path = os.path.join(folder_path, f"{original_name}_{filter_name}.png")
            cv2.imwrite(save_path, img)
        messagebox.showinfo("Saved", "All images saved successfully!")

    def update_filter_label(self):
        self.filter_label.configure(text=f"Current Filter: {self.filters_applied[self.current_index]}")

    def display_image(self):
        if not self.cv_images:
            return
        cv_image = self.cv_images[self.current_index]
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_image)

        cw, ch = self.canvas_frame.winfo_width() or 360, self.canvas_frame.winfo_height() or 500
        ir, cr = image.width / image.height, cw / ch

        if ir > cr:
            new_w, new_h = cw, int(cw / ir)
        else:
            new_h, new_w = ch, int(ch * ir)

        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.image)

    # ================= 필터 메서드 =================
    def apply_mosaic_filter(self): self.apply_filter(apply_mosaic_to_faces, "Mosaic")
    def apply_grayscale_filter(self): self.apply_filter(apply_grayscale, "Grayscale")
    def apply_cartoon_filter(self): self.apply_filter(apply_cartoon, "Cartoon")
    def apply_sketch_filter(self): self.apply_filter(apply_sketch, "Sketch")
    def apply_invert_filter(self): self.apply_filter(apply_invert, "Invert")
    def apply_blur_filter(self): self.apply_filter(apply_blur, "Blur")
    def apply_edge_filter(self): self.apply_filter(apply_edge_detection, "Edge")
    def apply_sepia_filter(self): self.apply_filter(apply_sepia, "Sepia")
    def apply_brightness_filter(self): self.apply_filter(apply_brightness, "Brightness")
    def apply_saturation_filter(self): self.apply_filter(apply_saturation, "Saturation")
    def apply_hdr_filter(self): self.apply_filter(apply_hdr_effect, "HDR")
    def apply_vignette_filter(self): self.apply_filter(apply_vignette, "Vignette")
    def apply_portrait_mode_filter(self): self.apply_filter(apply_portrait_mode, "Portrait Mode")
    def apply_remove_person_filter(self): self.apply_filter(apply_remove_person, "Remove Person")
    def apply_sticker_filter(self): self.apply_filter(apply_sticker, "Sticker")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
