from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")  # Load YOLO model


# IMAGE DETECTION
def detect_violation(image_path):
    image = cv2.imread(image_path)
    annotated_frame, violations = detect_violation_live(image)

    if len(violations) == 0:
        return "No Traffic Violation Detected"
    return ", ".join(list(set(violations)))


# ---------------- LIVE FRAME DETECTION ----------------
def detect_violation_live(frame):
    results = model(frame)

    violations = []
    motorcycles = []
    persons = []
    phones = []
    traffic_lights = []

    for r in results:
        boxes = r.boxes.xyxy
        classes = r.boxes.cls

        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = map(int, box)
            label = int(cls)

            if label == 0:  # person
                persons.append((x1, y1, x2, y2))
            elif label == 3:  # motorcycle
                motorcycles.append((x1, y1, x2, y2))
            elif label == 67:  # mobile phone
                phones.append((x1, y1, x2, y2))
            elif label == 9:  # traffic light
                traffic_lights.append((x1, y1, x2, y2))

    # TRIPLE RIDING
    for mx1, my1, mx2, my2 in motorcycles:
        rider_count = 0
        for px1, py1, px2, py2 in persons:
            if (px1 < mx2 and px2 > mx1 and py1 < my2 and py2 > my1):
                rider_count += 1

        if rider_count >= 3:
            violations.append("Triple Riding Violation")
        if rider_count >= 4:
            violations.append("Overcrowded Vehicle")

    # ---------------- HELMET VIOLATION ----------------
    if len(motorcycles) > 0 and len(persons) > 0:
        violations.append("No Helmet Detected")

    # MOBILE PHONE
    for mx1, my1, mx2, my2 in motorcycles:
        for px1, py1, px2, py2 in persons:
            if (px1 < mx2 and px2 > mx1 and py1 < my2 and py2 > my1):
                for phx1, phy1, phx2, phy2 in phones:
                    if (phx1 < px2 and phx2 > px1 and phy1 < py2 and phy2 > py1):
                        violations.append("Using Mobile While Driving")
                        break

    # STOP LINE
    height = frame.shape[0]
    stop_line = int(height * 0.80)
    bikes_before = 0
    bikes_after = 0

    for mx1, my1, mx2, my2 in motorcycles:
        if my2 < stop_line:
            bikes_before += 1
        else:
            bikes_after += 1

    if bikes_before >= 2 and bikes_after >= 1:
        violations.append("Stop Line Crossing")

    # RED LIGHT
    if len(traffic_lights) > 0 and bikes_after >= 1:
        violations.append("Red Light Jump")

    # ANNOTATE FRAME
    annotated_frame = frame.copy()
    for i, violation in enumerate(list(set(violations))):
        cv2.putText(
            annotated_frame,
            violation,
            (20, 40 + i * 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    return annotated_frame, list(set(violations))
