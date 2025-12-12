import platform
import ctypes
import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
# ... (필터 import 생략)
from filters.mosaic import apply_mosaic_to_faces
# ... (중략)
from PIL import Image, ImageTk
import numpy as np
import os

# 플랫폼별 DPI 인식 설정
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"DPI Awareness 설정 실패: {e}")


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Application")
        self.root.geometry("1000x800")
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # [추천 UI 변경 1]: 테마 설정 변경
        ctk.set_appearance_mode("Dark")
        # 'dark-blue' 테마를 사용하여 버튼과 강조 색상을 전문적인 청록색 계열로 설정
        ctk.set_default_color_theme("dark-blue") 

        self.images = []
        self.cv_images = []
        self.original_images = []
        self.original_file_paths = []
        self.current_index = 0
        self.filters_applied = []
        self.init_gui()

    def init_gui(self):
        # Title
        # [추천 UI 변경 2]: 타이틀 색상을 황금색(Gold)으로 변경하여 고급스러운 느낌 강조
        title_label = ctk.CTkLabel(self.root, text="Photo Filter Application", font=("Arial", 28, "bold"),
                                   text_color="#FFD700") # Gold 색상 (이전: #1abc9c)
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # Top buttons (Open, Save)
        button_frame_top = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame_top.grid(row=1, column=0, pady=5, sticky="ew")
        button_frame_top.columnconfigure((0, 1), weight=1)

        # [추천 UI 변경 3]: Open 버튼 색상을 테마 기본 색상인 진한 청록색(#2980b9 계열)으로 통일
        btn_open = ctk.CTkButton(button_frame_top, text="Open Images", command=self.open_images, width=150, # 너비도 약간 줄임
                                 fg_color="#2980b9") # (이전: #27ae60)
        btn_open.grid(row=0, column=0, padx=20, pady=10, sticky="w") # padx 증가

        # [추천 UI 변경 4]: Save 버튼 색상을 테마 기본 색상으로 통일
        btn_save = ctk.CTkButton(button_frame_top, text="Save All", command=self.save_all_images, width=150, # 너비도 약간 줄임
                                 fg_color="#2980b9") # (이전: #3498db)
        btn_save.grid(row=0, column=1, padx=20, pady=10, sticky="e") # padx 증가

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.canvas_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#333333", bd=0, highlightthickness=0) # [추천 UI 변경 5]: 캔버스 배경을 조금 더 어둡게 조정
        self.canvas.pack(fill="both", expand=True)

        # Canvas Navigation Buttons
        # [추천 UI 변경 6]: 네비게이션 버튼 투명도 및 디자인 개선
        self.left_button = ctk.CTkButton(self.canvas, text="<", width=40, height=40, corner_radius=20, # 둥근 모양 추가
                                        fg_color="rgba(0,0,0,0.4)", hover_color="rgba(0,0,0,0.6)", # 반투명한 배경색
                                        text_color="#FFFFFF", command=self.show_previous_image)
        self.right_button = ctk.CTkButton(self.canvas, text=">", width=40, height=40, corner_radius=20, # 둥근 모양 추가
                                         fg_color="rgba(0,0,0,0.4)", hover_color="rgba(0,0,0,0.6)", # 반투명한 배경색
                                         text_color="#FFFFFF", command=self.show_next_image)

        # Initially hide buttons
        self.left_button.place_forget()
        self.right_button.place_forget()

        # Canvas hover events
        self.canvas.bind("<Enter>", self.show_navigation_buttons)
        self.canvas.bind("<Leave>", self.hide_navigation_buttons)

        # Current Filter Label
        # [추천 UI 변경 7]: 현재 필터 라벨 색상을 황금색으로 변경하여 타이틀과 통일감 부여
        self.filter_label = ctk.CTkLabel(self.root, text=f"Current Filter: None",
                                         font=("Arial", 16, "bold"), text_color="#FFD700") # Gold 색상 (이전: #00d2d3)
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

        # [추천 UI 변경 8]: 버튼 너비를 줄여서 한 줄에 5개 버튼이 깔끔하게 보이도록 조정
        button_width = 120 
        for i, (text, command) in enumerate(filters):
            ctk.CTkButton(button_frame, text=f"{text} Filter", command=command, width=button_width).grid(
                row=i // 5, column=i % 5, padx=10, pady=5, sticky="nsew"
            )

        footer_label = ctk.CTkLabel(self.root, text="Tip: Load multiple images, apply filters, and save them!",
                                    font=("Arial", 14), text_color="#bdc3c7")
        footer_label.grid(row=5, column=0, pady=10, sticky="n")

    # ... (나머지 메서드 생략, 변경 사항 없음)
    def open_images(self):
        # ... (생략)
    def apply_filter(self, filter_function, filter_name):
        # ... (생략)
    def save_all_images(self):
        # ... (생략)
    def update_filter_label(self):
        # ... (생략)
    def display_image(self):
        # ... (생략)
    def show_previous_image(self):
        # ... (생략)
    def show_next_image(self):
        # ... (생략)
    def show_navigation_buttons(self, event):
        # ... (생략)
    def hide_navigation_buttons(self, event):
        # ... (생략)
    def apply_mosaic_filter(self):
        self.apply_filter(apply_mosaic_to_faces, "Mosaic")
    # ... (나머지 필터 메서드 생략)
    def apply_sticker_filter(self):
        self.apply_filter(apply_sticker, "Sticker")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FilterApp(root)
    root.mainloop()
