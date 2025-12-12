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

# 플랫폼별 DPI 인식 설정
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows DPI 인식 활성화
    except Exception as e:
        print(f"DPI Awareness 설정 실패: {e}")


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("1000x800")
        
        # UI/GUI 변수 정의 
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green") # Green 테마로 변경
        
        self.button_corner_radius = 12 # 버튼 둥글기 증가
        self.open_save_button_width = 250 # 버튼 크기 대폭 확대
        self.open_save_button_height = 50
        self.filter_button_width = 100
        self.filter_button_height = 40
        self.primary_color = "#2ECC71" # Open 버튼 색상 (밝은 초록)
        self.secondary_color = "#3498DB" # Save 버튼 색상 (밝은 파랑)
        self.title_color = "#ECF0F1" # 밝은 흰색

        # Grid 구성: 캔버스(row 2)와 하단 프레임(row 4)의 무게(weight)를 재정의
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1) # 캔버스 영역에 가장 큰 공간 할당
        self.root.rowconfigure(3, weight=0)
        self.root.rowconfigure(4, weight=0) # 하단 버튼 영역
        self.root.columnconfigure(0, weight=1)

        self.images = []
        self.cv_images = []
        self.original_images = []
        self.original_file_paths = []
        self.current_index = 0
        self.filters_applied = []
        self.init_gui()

    def init_gui(self):
        
        # 1. Title 및 Header 
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Arial", 20, "bold"),
                                   text_color=self.title_color)
        title_label.grid(row=0, column=0, pady=(15, 5), sticky="n")
        
        # 2. Top buttons (Open, Save) - 중앙에 크게 배치하여 핵심 기능 강조
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=10, sticky="n")
        button_frame_top.columnconfigure((0, 1), weight=1)

        btn_open = ctk.CTkButton(button_frame_top, text="Open Image", command=self.open_images, 
                                 width=self.open_save_button_width, height=self.open_save_button_height,
                                 corner_radius=self.button_corner_radius, font=("Arial", 16, "bold"),
                                 fg_color=self.primary_color, hover_color="#27AE60")
        # 중앙 배치
        btn_open.grid(row=0, column=0, padx=15, pady=5, sticky="e") 

        btn_save = ctk.CTkButton(button_frame_top, text="Save All", command=self.save_all_images,
                                 width=self.open_save_button_width, height=self.open_save_button_height,
                                 corner_radius=self.button_corner_radius, font=("Arial", 16, "bold"),
                                 fg_color=self.secondary_color, hover_color="#2980B9")
        # 중앙 배치
        btn_save.grid(row=0, column=1, padx=15, pady=5, sticky="w")
        
        # 3. Canvas Frame (이미지 표시 영역)
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=5, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#333333", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Canvas Navigation Buttons
        self.left_button = ctk.CTkButton(self.canvas, text="<", width=40, height=40, corner_radius=20, 
                                        fg_color="rgba(0,0,0,0.4)", hover_color="rgba(0,0,0,0.6)", 
                                        text_color="#FFFFFF", command=self.show_previous_image)
        self.right_button = ctk.CTkButton(self.canvas, text=">", width=40, height=40, corner_radius=20, 
                                         fg_color="rgba(0,0,0,0.4)", hover_color="rgba(0,0,0,0.6)", 
                                         text_color="#FFFFFF", command=self.show_next_image)

        self.left_button.place_forget()
        self.right_button.place_forget()
        self.canvas.bind("<Enter>", self.show_navigation_buttons)
        self.canvas.bind("<Leave>", self.hide_navigation_buttons)

        # Current Filter Label (캔버스 아래에 배치)
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: None",
                                         font=("Arial", 16), text_color=self.title_color)
        self.filter_label.grid(row=3, column=0, pady=5, sticky="n")

        # 4. Filter Buttons - 하단 고정 메뉴 (Bottom Bar) 스타일로 변경
        # 스크롤 가능하도록 CTkScrollableFrame 사용
        button_frame_scroll = ctk.CTkScrollableFrame(self.root, label_text="Select Filter",
                                                    label_text_color=self.primary_color,
                                                    fg_color="#2C3E50", # 짙은 회색 배경으로 하단 바 강조
                                                    orientation="horizontal", 
                                                    height=100) # 높이 지정
        
        button_frame_scroll.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        
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

        # 버튼을 가로로 길게 배치 (모바일 하단 메뉴처럼)
        for i, (text, command) in enumerate(filters):
            # 필터 버튼 스타일: 둥글고, 작고, 하단 바에 맞춤
            btn = ctk.CTkButton(button_frame_scroll, text=f"{text}", command=command, 
                                width=self.filter_button_width, height=self.filter_button_height,
                                corner_radius=self.button_corner_radius,
                                fg_color="#34495E") # 어두운 바에 맞는 배경색
            btn.grid(row=0, column=i, padx=8, pady=10) # row=0으로 고정하고 column만 증가

    def open_images(self):
        # 현재 스크립트의 디렉토리 기준으로 기본 폴더 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
        default_folder = os.path.join(script_dir, "../test_img")  # 상대 경로를 기준으로 기본 폴더 설정

        # 파일 대화 상자 열기
        file_paths = filedialog.askopenfilenames(
            initialdir=default_folder,  # 기본 폴더 설정
            filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
        )
        if not file_paths:
            return

        self.cv_images.clear()
        self.original_images.clear()
        self.original_file_paths.clear()
        self.filters_applied.clear()

        for file_path in file_paths:
            try:
                file_data = np.fromfile(file_path, dtype=np.uint8)
                image = cv2.imdecode(file_data, cv2.IMREAD_COLOR)
                if image is None:
                    raise ValueError(f"Failed to decode {file_path}")
                self.original_images.append(image)
                self.cv_images.append(image.copy())
                self.original_file_paths.append(file_path)
                self.filters_applied.append("None")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {file_path}: {e}")

        self.current_index = 0
        self.update_filter_label()
        self.display_image()

    def apply_filter(self, filter_function, filter_name):
        if not self.cv_images:
            messagebox.showwarning("Warning", "No images loaded!")
            return

        if self.filters_applied[self.current_index] == filter_name:
            self.cv_images[self.current_index] = self.original_images[self.current_index].copy()
            self.filters_applied[self.current_index] = "None"
        else:
            self.cv_images[self.current_index] = filter_function(self.original_images[self.current_index].copy())
            self.filters_applied[self.current_index] = filter_name

        self.update_filter_label()
        self.display_image()

    def save_all_images(self):
        if not self.cv_images:
            messagebox.showwarning("Warning", "No images to save!")
            return

        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        for idx, image in enumerate(self.cv_images):
            original_name = os.path.splitext(os.path.basename(self.original_file_paths[idx]))[0]
            filter_name = self.filters_applied[idx] if self.filters_applied[idx] != "None" else "original"
            save_path = os.path.join(folder_path, f"{original_name}_{filter_name}.png")
            cv2.imwrite(save_path, image)

        messagebox.showinfo("Info", "All images saved successfully!")

    def update_filter_label(self):
        current_filter = self.filters_applied[self.current_index]
        self.filter_label.configure(text=f"Current Filter: {current_filter}")

    def display_image(self):
        if not self.cv_images:
            return

        cv_image = self.cv_images[self.current_index]
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_image)
        canvas_width, canvas_height = self.canvas_frame.winfo_width(), self.canvas_frame.winfo_height()
        image_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height

        if image_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / image_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * image_ratio)

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.image)

    def show_previous_image(self):
        if not self.cv_images:
            messagebox.showwarning("Warning", "No images loaded!")
            return
        self.current_index = (self.current_index - 1) % len(self.cv_images)
        self.update_filter_label()
        self.display_image()

    def show_next_image(self):
        if not self.cv_images:
            messagebox.showwarning("Warning", "No images loaded!")
            return
        self.current_index = (self.current_index + 1) % len(self.cv_images)
        self.update_filter_label()
        self.display_image()

    def show_navigation_buttons(self, event):
        hwnd = self.canvas.winfo_id()
        dpi = 96
        if platform.system() == "Windows":
            dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
        scale_factor = dpi / 96

        canvas_width = int(self.canvas.winfo_width() / scale_factor)
        canvas_height = int(self.canvas.winfo_height() / scale_factor)

        self.left_button.update_idletasks()
        self.right_button.update_idletasks()

        button_y_position = canvas_height // 2

        self.left_button.place(x=10, y=button_y_position, anchor="w")
        self.right_button.place(x=canvas_width - 10, y=button_y_position, anchor="e")

    def hide_navigation_buttons(self, event):
        self.left_button.place_forget()
        self.right_button.place_forget()

    def apply_mosaic_filter(self):
        self.apply_filter(apply_mosaic_to_faces, "Mosaic")

    def apply_grayscale_filter(self):
        self.apply_filter(apply_grayscale, "Grayscale")

    def apply_cartoon_filter(self):
        self.apply_filter(apply_cartoon, "Cartoon")

    def apply_sketch_filter(self):
        self.apply_filter(apply_sketch, "Sketch")

    def apply_invert_filter(self):
        self.apply_filter(apply_invert, "Invert")

    def apply_blur_filter(self):
        self.apply_filter(apply_blur, "Blur")

    def apply_edge_filter(self):
        self.apply_filter(apply_edge_detection, "Edge")

    def apply_sepia_filter(self):
        self.apply_filter(apply_sepia, "Sepia")

    def apply_brightness_filter(self):
        self.apply_filter(apply_brightness, "Brightness")

    def apply_saturation_filter(self):
        self.apply_filter(apply_saturation, "Saturation")

    def apply_hdr_filter(self):
        self.apply_filter(apply_hdr_effect, "HDR")

    def apply_vignette_filter(self):
        self.apply_filter(apply_vignette, "Vignette")

    def apply_portrait_mode_filter(self):
        self.apply_filter(apply_portrait_mode, "Portrait Mode")

    def apply_remove_person_filter(self):
        self.apply_filter(apply_remove_person, "Remove Person")

    def apply_sticker_filter(self):
        self.apply_filter(apply_sticker, "Sticker")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
