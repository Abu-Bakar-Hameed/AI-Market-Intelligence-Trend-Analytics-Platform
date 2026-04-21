# AI-Market-Intelligence-Trend-Analytics-Platform
# 🚀 AI-Powered Market Intelligence & Trend Analytics Platform

## 📌 Project Overview

This project is a **production-grade backend system** built using FastAPI that collects real-world data from a third-party API, processes it, stores it in MongoDB, and provides analytical insights through REST APIs.

The system performs:

* Data ingestion from external APIs
* Data cleaning and normalization
* Keyword extraction and sentiment analysis
* Trend detection and analytics
* Public API exposure with FastAPI

---

## 🎯 Objective

To build a scalable backend system that:

* Integrates real-world APIs
* Processes unstructured data
* Performs analytics and trend detection
* Exposes insights via REST APIs
* Is deployed and publicly accessible

---

## 🧠 Features

### ✅ Core Features

* Data ingestion from News API
* MongoDB Atlas integration
* Data processing pipeline
* Keyword extraction
* Sentiment analysis (rule-based)
* Trend scoring system
* REST API using FastAPI

### ⚡ Advanced Features

* Background task processing (FastAPI)
* Logging system
* Error handling & validation


---

## 🏗️ System Architecture

```
Client Request
     ↓
FastAPI Backend
     ↓
Data Ingestion Service (News API)
     ↓
MongoDB Atlas (Raw Data)
     ↓
Data Processing Pipeline
     ↓
MongoDB Atlas (Processed Data)
     ↓
Analytics Engine
     ↓
API Response (JSON)
```

---

## 🌐 Third-Party API Used

* News API (for real-time news data)

---

## 🧩 Functional Modules

### 1. Data Ingestion

* Fetch data from API
* Normalize and clean data
* Store in `raw_data` collection

### 2. Data Processing

* Extract keywords
* Perform sentiment analysis
* Calculate trend score
* Store in `processed_data`

---

## 🗄️ Database Schema

### Raw Data Collection (`raw_data`)

```json
{
  "title": "AI is growing fast",
  "source": "BBC",
  "published_at": "2026-04-20",
  "content": "Full article text...",
  "category": "technology"
}
```

---

### Processed Data Collection (`processed_data`)

```json
{
  "title": "AI is growing fast",
  "sentiment": "positive",
  "keywords": ["AI", "technology"],
  "score": 0.87,
  "trend_score": 12
}
```

---

## 📊 Data Analysis Features

### 🔥 Trend Detection

* Top keywords (last 24 hours / 7 days)

### 😊 Sentiment Analysis

* Positive
* Negative
* Neutral

### 📈 Time-Series Analysis

* Daily data counts
* Growth trends

---

## ⚡ API Endpoints

### 📥 POST `/ingest`

Fetch and store data from API

**Response:**

```json
{
  "message": "Data ingested successfully"
}
```

---

### 📊 GET `/trends?days=7`

Get trending keywords

**Response:**

```json
{
  "trends": [
    {"keyword": "AI", "count": 120}
  ]
}
```

---

### 📈 GET `/insights`

Get aggregated insights

---

### 🔍 GET `/search?q=keyword`

Search data by keyword

---

### 📉 GET `/analytics/summary`

Get summary statistics

---

## ⚙️ Tech Stack

* FastAPI
* MongoDB Atlas
* Python
* Uvicorn / Gunicorn
* Pydantic

