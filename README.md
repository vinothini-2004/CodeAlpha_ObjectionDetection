# 🎯 Object Detection & Tracking
**YOLOv8 + SORT (Simple Online Realtime Tracking)**

Real-time object detection and tracking from webcam, video file, or synthetic demo — with bounding boxes, class labels, unique tracking IDs, and motion trails.

---

## 📁 Project Structure

```
object_detection_tracking/
├── main.py                    ← Main entry point
├── generate_sample_output.py  ← Generate sample output image
├── requirements.txt
├── tracker/
│   ├── __init__.py
│   └── sort.py                ← SORT tracker (Kalman + Hungarian)
└── output/                    ← Auto-created; saved videos & images go here
```

---

## ⚙️ Step-by-Step Setup & Run

### Step 1 — Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

Check your Python version:
```bash
python --version
```

---

### Step 2 — Create a virtual environment (recommended)
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS / Linux)
source venv/bin/activate
```

---

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** `ultralytics` will automatically download the YOLOv8n weights (~6 MB)
> on the first run. An internet connection is required for that one-time download.

---

### Step 4 — Run the project

#### Option A — Webcam (default)
```bash
python main.py --source 0
```
Uses your default webcam. Use `--source 1` for a secondary camera.

#### Option B — Video file
```bash
python main.py --source path/to/your/video.mp4
```

#### Option C — Demo mode (NO camera / video needed)
```bash
python main.py --demo
```
Runs with synthetic moving objects — perfect for testing on any machine.

#### Option D — Save output video
```bash
python main.py --source 0 --save
# Saved to: output/tracked_output.mp4
```

#### Option E — Headless mode (server / no display)
```bash
python main.py --demo --headless --headless_frames 120
```

---

### Step 5 — Generate sample output image
```bash
python generate_sample_output.py
# Saved to: output/sample_output.png
#           output/legend.png
```

---

## 🎛️ All Command-Line Arguments

| Argument | Default | Description |
|---|---|---|
| `--source` | `0` | `0` = webcam, `1` = second cam, or path to video file |
| `--model` | `yolov8n.pt` | YOLO model: `yolov8n`, `yolov8s`, `yolov8m`, `yolov8l`, `yolov8x` |
| `--conf` | `0.4` | Detection confidence threshold (0.0 – 1.0) |
| `--width` | `960` | Frame width (pixels) |
| `--height` | `540` | Frame height (pixels) |
| `--save` | off | Save output to `output/tracked_output.mp4` |
| `--demo` | off | Run synthetic demo (no camera required) |
| `--headless` | off | No GUI window (for servers/CI) |
| `--headless_frames` | `90` | Number of frames to process in headless mode |

---

## 🖥️ What You'll See

| Visual Element | Description |
|---|---|
| **Bounding box** | Coloured rectangle around each detected object |
| **Label pill** | `ID:N ClassName ConfScore` above each box |
| **Motion trail** | Fading coloured line showing recent movement path |
| **HUD (top-left)** | Live FPS, detection count, tracking count, mode |

**Controls:**
- Press **Q** to quit

---

## 🔧 Model Size vs Speed

| Model | Size | Speed (CPU) | Accuracy |
|---|---|---|---|
| `yolov8n.pt` | ~6 MB  | ~25 FPS | Good |
| `yolov8s.pt` | ~22 MB | ~18 FPS | Better |
| `yolov8m.pt` | ~50 MB | ~10 FPS | Even better |
| `yolov8l.pt` | ~87 MB | ~6 FPS  | High |
| `yolov8x.pt` | ~130 MB| ~4 FPS  | Highest |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `No module named 'ultralytics'` | Run `pip install ultralytics` |
| Camera not opening | Try `--source 1` or check device permissions |
| Slow FPS | Use `--model yolov8n.pt` (default, fastest) |
| No display on server | Add `--headless` flag |
| CUDA/GPU not used | Install `torch` with CUDA support from pytorch.org |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `opencv-python` | Video capture, frame rendering |
| `ultralytics` | YOLOv8 detection model |
| `numpy` | Matrix operations |
| `scipy` | Hungarian algorithm for SORT assignment |

SORT tracker is **bundled** — no separate install needed.
