# TaskSight AI

## Human vs AI Attention Analysis Platform

TaskSight AI is an AI-powered visual attention analysis platform that compares human-selected regions of interest with AI-detected objects and attention patterns.

The system combines computer vision, object detection, image captioning, and visual question answering to analyze how humans and AI interpret the same image.

---

## Features

* Human Attention Selection using interactive bounding boxes
* YOLOv8 Object Detection
* AI Attention Visualization
* Human vs AI Overlay Comparison
* Agreement Score Calculation (IoU Based)
* Image Caption Generation using BLIP
* Visual Question Answering
* Experiment History Tracking
* Downloadable Experiment Reports
* Dark Mode Support

---

## Tech Stack

### Frontend

* React
* Axios
* CSS

### Backend

* FastAPI
* Python

### AI Models

* YOLOv8
* BLIP Captioning
* BLIP VQA

### Database

* SQLite

---

## Project Architecture

User Uploads Image

↓

React Frontend

↓

FastAPI Backend

↓

YOLO + BLIP Processing

↓

SQLite Logging

↓

Visualization & Analysis Results

---

## Outputs Generated

* Human Attention Region
* AI Attention Map
* YOLO Object Detection
* Human vs AI Overlay
* Agreement Score
* Caption Generation
* Scene Understanding
* Object Counting
* Risk Detection
* Spatial Reasoning

---

## How To Run

### Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Author

Apurva Sharma

B.Tech Electronics Engineering (AI/ML Minor)

VJTI Mumbai
