# Face Recognition System

This repository provides a face recognition system that allows for registering faces into a database and later finding similar faces in that database using a ML AdaFace model, Yolo model and onnx model. The system is built using PyTorch and offers various functionalities including live webcam-based registration and recognition.

## Setup

1. **Clone the Repository**
   ```bash
   git clone -b frs_modules https://gitlab.com/essi-tech/facenetmatch.git
   cd facenetmatch
   ```

2. **Download the Models**

   To run the face recognition, detection, and liveness detection features, you'll need to download the trained ML models from Google Drive and place them in the appropriate directories.
   
   Google drive link: `https://drive.google.com/drive/folders/1sOiR61bgu5OftQLCBX45XISLNXDIj4th?usp=sharing`

```bash
   facenetmatch/
   │
   ├── model/
   │   ├── final_faceDet_model.pt
   │   ├── adaface_ir101_webface12m.ckpt
   │
   └── scripts/
      └── facetools/
         └── checkpoints/
               └── OULU_Protocol_2_model_0_0.onnx
```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   ***After that, install the appropriate version of PyTorch based on your CUDA version. For CUDA 11.5, you can run:***
  `pip install torch==2.4.1+cu115 torchvision==0.19.1+cu115 -f https://download.pytorch.org/whl/torch_stable.html`


## Usage

The system offers several modes of operation:

### 1. Register Faces from Image

To register faces from an image into the SQLite database:

```bash
python main.py --reg --img_path <image_path> --person_name <name>
```

### 2. Find Similar Faces

To find similar faces in the database based on an input image:

```bash
python main.py --find --input_image <image_path>
```

### 3. Webcam-based Face Recognition

To run face recognition on a live webcam feed:

```bash
python main.py --webcam_find
```

### 4. Webcam-based Face Registration

To register faces via webcam:

```bash
python main.py --webcam_reg
```

### 5. Webcam-based Registration and Recognition

To both register and recognize faces via webcam:

```bash
python main.py --webcam_frs
```

This mode (implemented in `find_nd_reg.py`) allows you to:
- Register new faces by pressing 'c' when a face is detected
- Recognize registered faces in real-time
- Delete registered faces by pressing 'd' and entering the face ID

## Additional Information

- The system uses CUDA if available, otherwise it defaults to CPU.
- The face detection model path is specified in the code. Ensure this path is correct for your setup.
- The database path can be specified with the `--db_path` argument (default is "face_features.db").

## Notes

- Ensure proper lighting and face positioning for optimal performance.
- The system includes liveness detection to prevent spoofing.
- When using webcam modes, follow on-screen instructions for registration and deletion of faces.

For any issues or further information, please refer to the documentation or contact the repository maintainer.