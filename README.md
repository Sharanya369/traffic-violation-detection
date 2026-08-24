# Smart Traffic Violation Detection Using CV & AI

A real-time traffic violation detection system built with YOLOv8, OpenCV, and Flask. 
Detects helmet violations, triple riding, mobile phone usage while driving, stop-line 
crossing, and red-light jumping — from either an uploaded image or a live webcam feed.

## Features
- **Image upload detection** — upload a traffic photo and get instant violation results
- **Live camera detection** — stream your webcam and detect violations in real time
- **Detection history** — every flagged violation is logged with a snapshot and timestamp
- **Web dashboard** — simple Flask-based UI to view results and history

## Violations Detected
| Violation | Logic |
|---|---|
| No Helmet Detected | Motorcycle + rider present, no helmet class matched |
| Triple Riding | 3+ person boxes overlapping a single motorcycle box |
| Overcrowded Vehicle | 4+ person boxes overlapping a single motorcycle box |
| Using Mobile While Driving | Phone bounding box overlaps a rider on a motorcycle |
| Stop Line Crossing | Motorcycles detected past a defined stop-line threshold |
| Red Light Jump | Traffic light detected + vehicle past the stop line |

## Tech Stack
- **Detection model:** YOLOv8 (Ultralytics)
- **Computer Vision:** OpenCV
- **Backend:** Flask
- **Frontend:** HTML, CSS, Jinja2 templates

## Project Structure
## How It Works
1. A frame (from an uploaded image or live camera) is passed to a YOLOv8 model
2. The model detects people, motorcycles, mobile phones, and traffic lights
3. Bounding box overlap logic checks for violations (e.g., a phone box overlapping 
   a rider box on a motorcycle → "Using Mobile While Driving")
4. Detected violations are annotated on the frame and logged with a timestamp

## Setup
```bash
git clone https://github.com/Sharanya369/traffic-violation-detection.git
cd traffic-violation-detection
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## Results
Tested across light, moderate, and heavy traffic conditions:
- Vehicle detection accuracy: 92–98% depending on traffic density
- Vehicle counting accuracy: 90–97%
- Traffic density classification accuracy: 92–100%

## Future Enhancements
- Speed violation detection using frame-to-frame displacement
- License plate recognition for automated penalty issuance
- Integration with adaptive traffic signal control

## Team
Developed as a final-year B.Tech project by M. Poojitha, O. Harshini, G. Poorna Chandrarao, 
and G. Sharanya, under the guidance of Mr. B. Balaji, Dept. of CSE (IoT & Cybersecurity 
including Blockchain Technology), Amrita Sai Institute of Science and Technology.
