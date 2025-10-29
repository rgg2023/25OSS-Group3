<p align="center">
  <h1>Photo Filter Application with OpenCV (Mosaic & More)</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/OpenCV-4.8.0-green?logo=opencv&logoColor=white" alt="OpenCV 4.8.0">
  <img src="https://img.shields.io/badge/IDE-PyCharm-000000?logo=pycharm&logoColor=white" alt="PyCharm">
  <img src="https://img.shields.io/badge/License-MIT-yellow?logo=license&logoColor=white" alt="MIT License">
</p>

<p>
  <i>* Note: It is optional but highly recommended to use <b>PyCharm</b> as the development environment for this project. PyCharm provides excellent tools for managing virtual environments, debugging, and organizing code efficiently.</i>
</p>

# 24OSS-Group26  
**Photo Filter Application with OpenCV (Mosaic & More)**

## Project Overview
This repository is dedicated to the Group 26 term project for the **Open Source Software Course, 2024**, at **Gachon University**. Our project involves applying various filters, such as mosaic effects, to photos using OpenCV. Through this project, we aim to explore image processing techniques in an open-source context.


## Team Members
| Name | GitHub Profile                                                                                                           | Email                                                                                              |
|------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| 김효현  | [<img src="https://img.shields.io/badge/GitHub-rgg2023-black?logo=github" alt="rgg2023">](https://github.com/rgg2023)    | <img src="https://img.shields.io/badge/gyguspr@gachon.ac.kr-blue" alt="gyguspr@gachon.ac.kr">      |
|      | [<img src="https://img.shields.io/badge/GitHub--black?logo=github" alt="">](https://github.com/cire21st) | <img src="https://img.shields.io/badge/-blue" alt="">        |
|      | [<img src="https://img.shields.io/badge/GitHub--black?logo=github" alt="">](https://github.com/yeun23)       | <img src="https://img.shields.io/badge/-blue" alt=""> | 


## Project Structure
The directory structure for this repository is as follows:

<pre>
25OSS-Group3/
├── src/
│   ├── filters/                  # Contains Python scripts for each filter
│   │   ├── blur.py               # Blur filter
│   │   ├── brightness.py         # Brightness adjustment filter
│   │   ├── cartoon.py            # Cartoon effect filter
│   │   ├── edge_detection.py     # Edge detection filter
│   │   ├── grayscale.py          # Grayscale filter
│   │   ├── hdr_effect.py         # HDR effect filter
│   │   ├── invert.py             # Invert colors filter
│   │   ├── mosaic.py             # Mosaic (pixelation) filter for face anonymization
│   │   ├── portrait_mode.py      # Portrait Mode filter with background blur
│   │   ├── remove_person.py      # Person removal filter
│   │   ├── saturation.py         # Saturation adjustment filter
│   │   ├── sepia.py              # Sepia tone filter
│   │   ├── sketch.py             # Pencil sketch effect filter
│   │   ├── sticker.py            # Sticker filter to add stickers to faces
│   │   └── vignette.py           # Vignette effect filter
│   └── main.py                   # Main script for filter selection and application
├── gif/                          # Contains scripts and screenshots to create GIFs
│   ├── create_gif.py             # Python script to create GIFs
│   └── output.gif                # Generated GIF example
├── test_img/                     # Directory containing sample images
├── requirements.txt              # List of dependencies (auto-generated)
├── generate_requirements.py      # Python script to generate requirements.txt
├── README.md                     # Project documentation
└── LICENSE                       # License information
</pre>

- **`src/filters/`**: Contains Python scripts for various image processing filters like blur, brightness adjustment, cartoon effect, etc.
  - **`blur.py`**: Applies a blur effect to the image.
  - **`brightness.py`**: Adjusts the brightness of the image.
  - **`cartoon.py`**: Converts the image to a cartoon-style effect.
  - **`edge_detection.py`**: Detects edges in the image.
  - **`grayscale.py`**: Converts the image to grayscale.
  - **`hdr_effect.py`**: Adds a high dynamic range (HDR) effect.
  - **`invert.py`**: Inverts the colors of the image.
  - **`mosaic.py`**: Detects faces and applies a mosaic (pixelation) effect for anonymization.
  - **`portrait_mode.py`**: Simulates portrait mode by blurring the background while keeping the person in focus.
  - **`remove_person.py`**: Removes a detected person from the image and fills the background.
  - **`saturation.py`**: Adjusts the saturation levels of the image.
  - **`sepia.py`**: Applies a sepia tone effect.
  - **`sketch.py`**: Converts the image to a pencil sketch effect.
  - **`sticker.py`**: Detects faces and places a sticker on each detected face.
  - **`vignette.py`**: Adds a vignette effect (darkened edges around the image).

- **`src/main.py`**: The main script that provides a GUI interface for applying the filters interactively. Users can open an image, apply filters, and save the results.

- **`gif/`**: Includes scripts for creating GIFs and example outputs.
  - **`create_gif.py`**: A Python script to create GIF animations showcasing filter application.
  - **`output.gif`**: An example of a generated GIF.

- **`test_img/`**: A directory containing sample images to demonstrate the effects of the filters.

- **`generate_requirements.py`**: A script that generates a `requirements.txt` file based on the installed Python packages in the environment.

- **`requirements.txt`**: A file listing all the required dependencies for running the project, including Python libraries like OpenCV, TensorFlow, and CustomTkinter.

- **`README.md`**: The main documentation file that provides an overview of the project, usage instructions, and details about each component.

- **`LICENSE`**: Contains the open-source license information for the project.



## Getting Started

0. **Use PyCharm and Set Up a New Virtual Environment (Recommended)**  
   - It is recommended to use **PyCharm** for better project management and debugging experience. Within PyCharm, create a **new virtual environment** to ensure that all dependencies are isolated for this project.  
   - To set up a new virtual environment in PyCharm:  
     1. Go to **File > Settings > Project: <Project Name> > Python Interpreter**.  
     2. Click the **gear icon** and select **Add...**.  
     3. Choose **New Virtual Environment**, specify the location, and ensure you select **Python 3.12** as the interpreter.  
     4. Click **OK** to create the environment.  

   <p align="left">
     <i>*Note: The instructions below are based on this setup and assume you are working in a new virtual environment within PyCharm with Python 3.12.</i>
   </p>

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/24OSS-Group26/24OSS-Group26.git
   ```
   
2. **Navigate to the Project Directory**  
   Change to the project directory:
   ```bash
   cd 24OSS-Group26
   ```

3. **Install Dependencies**  
   Install the required libraries (Python 3.12 and OpenCV):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**  
   Navigate to the `src` folder and run `main.py` to start applying filters:
   ```bash
   cd src
   python main.py
   ```

## Features
- **Mosaic Filter**: Detect faces in an image and apply a pixelation (mosaic) effect specifically to those areas. If multiple faces are detected, the filter applies the mosaic effect to all detected faces. This ensures privacy or artistic effects while leaving the rest of the image intact.
- **Additional Filters**: Explore more effects such as grayscale, sepia, and more.

## Usage
Run the `main.py` script in the `src` folder to select and apply various filters to images. Follow the instructions in the script for filter selection and intensity adjustment.

## Screenshot Example
Here are example images after applying the filter:

<p align="center">
  <img src="README_img/12.png" alt="Filter Example png 1">
  <img src="README_img/13.png" alt="Filter Example png 2">
  <img src="README_img/14.png" alt="Filter Example png 3">
  <img src="README_img/gif/output_20241118_195110.gif" alt="Filter Example gif 1">
  <img src="README_img/15.png" alt="Filter Example png 4">
  <img src="README_img/18.png" alt="Filter Example png 5">
  <img src="README_img/19.png" alt="Filter Example png 6">
</p>