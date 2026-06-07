"""
generate_sample_output.py
Generates a realistic sample output frame (no camera/model needed).
Run: python generate_sample_output.py
"""

import cv2
import numpy as np
import os

W, H = 960, 540

COCO_CLASSES = [
    "person","bicycle","car","motorbike","aeroplane","bus","train","truck",
    "boat","traffic light","fire hydrant","stop sign","parking meter","bench",
    "bird","cat","dog","horse","sheep","cow"
]
np.random.seed(42)
COLORS = np.random.randint(50, 230, size=(len(COCO_CLASSES), 3)).tolist()


def draw_box(img, x1, y1, x2, y2, tid, cls_id, conf, trail=None):
    color = tuple(COLORS[cls_id % len(COLORS)])
    label = f"ID:{tid}  {COCO_CLASSES[cls_id]}  {conf:.0%}"
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    cv2.rectangle(img, (x1, y1-th-8), (x1+tw+6, y1), color, -1)
    cv2.putText(img, label, (x1+3, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 2)
    if trail:
        for i in range(1, len(trail)):
            alpha = i / len(trail)
            tc = tuple(int(c * alpha) for c in color)
            cv2.line(img, trail[i-1], trail[i], tc, 2)


def main():
    os.makedirs("output", exist_ok=True)

    # ── background: a simple "road scene" ────────────────────────────────────
    frame = np.zeros((H, W, 3), dtype=np.uint8)
    # sky
    frame[:H//2, :] = (140, 100, 60)
    # road
    frame[H//2:, :] = (80, 80, 80)
    # road markings
    for x in range(0, W, 60):
        cv2.rectangle(frame, (x, H//2+20), (x+35, H//2+28), (220,220,220), -1)
    # horizon line
    cv2.line(frame, (0, H//2), (W, H//2), (60,60,60), 2)

    # ── tracked objects ───────────────────────────────────────────────────────
    objects = [
        # (x1, y1, x2, y2, tid, cls_id, conf, trail_pts)
        (60,  170, 180, 430, 1, 0, 0.91,
         [(70,430),(90,420),(100,400),(110,380),(120,360),(130,340)]),

        (240, 280, 500, 430, 2, 2, 0.87,
         [(260,430),(300,428),(340,425),(370,422),(400,420),(430,418)]),

        (560, 200, 720, 430, 3, 0, 0.83,
         [(580,430),(590,415),(600,398),(610,380),(615,360),(618,340)]),

        (730, 300, 940, 430, 4, 3, 0.78,
         [(740,430),(760,428),(790,425),(820,422),(850,420),(880,418)]),

        (300, 170, 420, 300, 5,  7, 0.72,
         [(320,300),(330,285),(340,270),(350,258),(360,248),(370,238)]),
    ]

    for (x1,y1,x2,y2,tid,cls_id,conf,trail) in objects:
        draw_box(frame, x1, y1, x2, y2, tid, cls_id, conf, trail)

    # ── HUD ──────────────────────────────────────────────────────────────────
    cv2.rectangle(frame, (0,0), (310, 85), (20,20,20), -1)
    cv2.putText(frame, "FPS : 28.4",      (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),  2)
    cv2.putText(frame, "Det : 5",          (8, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,200,255),2)
    cv2.putText(frame, "Trk : 5",          (8, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,200,0),2)
    cv2.putText(frame, "[YOLOv8n+SORT]", (130, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55,(200,100,255),2)

    # ── title banner ─────────────────────────────────────────────────────────
    cv2.rectangle(frame, (0, H-38), (W, H), (10,10,10), -1)
    cv2.putText(frame,
                "Object Detection & Tracking  |  YOLOv8 + SORT  |  Sample Output",
                (10, H-12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

    out = "output/sample_output.png"
    cv2.imwrite(out, frame)
    print(f"[OK] Saved → {out}")

    # ── also save a legend image ──────────────────────────────────────────────
    legend = np.zeros((200, 400, 3), dtype=np.uint8)
    legend[:] = (25,25,25)
    cv2.putText(legend, "Legend", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    items = [
        ("Bounding box + class label", (0,200,255)),
        ("Unique tracking ID (ID:N)", (0,255,0)),
        ("Motion trail (history)", (255,200,0)),
        ("HUD: FPS / Det / Trk count", (200,100,255)),
    ]
    for i,(txt,col) in enumerate(items):
        y = 60 + i*33
        cv2.rectangle(legend, (10,y-12),(22,y+2), col, -1)
        cv2.putText(legend, txt, (30,y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (220,220,220), 1)
    cv2.imwrite("output/legend.png", legend)
    print("[OK] Saved → output/legend.png")


if __name__ == "__main__":
    main()
