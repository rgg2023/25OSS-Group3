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
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.images = []  # 여러 장의 이미지를 저장할 리스트
        self.cv_images = []  # OpenCV 이미지 저장
        self.original_images = []  # 원본 이미지 저장
        self.original_file_paths = []  # 파일 경로 저장
        self.current_index = 0  # 현재 표시 중인 이미지 인덱스
        self.filters_applied = []  # 각 이미지에 적용된 필터 이름 리스트
        self.init_gui()

    def init_gui(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Arial", 28, "bold"),
                                   text_color="#1abc9c")
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Top buttons (Open, Save)
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=5, sticky="ew")
        button_frame_top.columnconfigure((0, 1), weight=1)

        btn_open = ctk.CTkButton(button_frame_top, text="Open Images", command=self.open_images, width=180,
                                 fg_color="#27ae60")
        btn_open.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        btn_save = ctk.CTkButton(button_frame_top, text="Save All", command=self.save_all_images, width=180,
                                 fg_color="#3498db")
        btn_save.grid(row=0, column=1, padx=15, pady=10, sticky="e")

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Canvas Navigation Buttons
        self.left_button = ctk.CTkButton(self.canvas, text="<", width=40, command=self.show_previous_image)
        self.right_button = ctk.CTkButton(self.canvas, text=">", width=40, command=self.show_next_image)

        # Initially hide buttons
        self.left_button.place_forget()
        self.right_button.place_forget()

        # Canvas hover events
        self.canvas.bind("<Enter>", self.show_navigation_buttons)
        self.canvas.bind("<Leave>", self.hide_navigation_buttons)

        # Current Filter Label
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: None",
                                         font=("Arial", 16), text_color="#00d2d3")
        self.filter_label.grid(row=3, column=0, pady=5, sticky="n")

        # Filter Buttons
        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        filters = [
            ("Mosaic", self.apply_mosaic_filter),
            ("Grayscale", self.apply_grayscale_filter),
            ("Cartoon", self.apply_cartoon_filter),
            ("Sketch", self.apply_sketch_filter),
            ("Invert", self.apply_invert_filter),
            ("Blur", self.apply_blur_filter),
            ("Edge", self.apply_edge_filter),
            ("Sepia", self.apply_sepia_filter),
            ("Brightness", self.apply_brightness_filter),
            ("Saturation", self.apply_saturation_filter),
            ("HDR", self.apply_hdr_filter),
            ("Vignette", self.apply_vignette_filter),
            ("Portrait Mode", self.apply_portrait_mode_filter),
            ("Remove Person", self.apply_remove_person_filter),
            ("Sticker", self.apply_sticker_filter),
        ]

        button_width = 180
        for i, (text, command) in enumerate(filters):
            ctk.CTkButton(button_frame, text=f"{text} Filter", command=command, width=button_width).grid(
                row=i // 5, column=i % 5, padx=10, pady=5, sticky="nsew"
            )

        footer_label = ctk.CTkLabel(self.root, text="Tip: Load multiple images, apply filters, and save them!",
                                    font=("Arial", 14), text_color="#bdc3c7")
        footer_label.grid(row=5, column=0, pady=10, sticky="n")

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
        dpi = 96  # 기본 DPI 값
        if platform.system() == "Windows":
            dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
        scale_factor = dpi / 96

        # 캔버스 크기 계산 (배율 적용)
        canvas_width = int(self.canvas.winfo_width() / scale_factor)
        canvas_height = int(self.canvas.winfo_height() / scale_factor)

        # 버튼 높이를 계산하기 전에 렌더링
        self.left_button.update_idletasks()
        self.right_button.update_idletasks()

        # 버튼 세로 중심 계산
        button_y_position = canvas_height // 2

        # 왼쪽 버튼 배치
        self.left_button.place(
            x=10,  # 고정된 X축 오프셋
            y=button_y_position,
            anchor="w"  # 왼쪽 기준
        )

        # 오른쪽 버튼 배치
        self.right_button.place(
            x=canvas_width - 10,  # 오른쪽 경계에서 오프셋
            y=button_y_position,
            anchor="e"  # 오른쪽 기준
        )

        # 디버깅 출력 주석으로 내비둠
        #print(f"DPI: {dpi}, Scale Factor: {scale_factor}")
        #print(f"Canvas Width (Scaled): {canvas_width}, Canvas Height (Scaled): {canvas_height}")
        #print(f"Button Y Position: {button_y_position}")
        #print(f"Left Button: {self.left_button.place_info()}")
        #print(f"Right Button: {self.right_button.place_info()}")

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
