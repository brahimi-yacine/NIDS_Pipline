# NIDS Pipeline – CIC-IDS2017

## Project Overview
This project implements a Network Intrusion Detection System (NIDS) using machine learning techniques on the CIC-IDS2017 dataset.  
The goal is to preprocess network traffic data, train a classification model, evaluate its performance, and perform intrusion detection on new traffic data.

---

## Dataset
- Name: CIC-IDS2017  
- Source: Canadian Institute for Cybersecurity (CIC)  
- Type: Network flow-based traffic data  
- Classes: BENIGN and multiple attack types (DoS, DDoS, PortScan, Bot, etc.)

> The raw dataset is not included in this repository due to its large size.

---

## Machine Learning Pipeline
The implemented pipeline consists of:
1. StandardScaler – feature normalization  
2. SelectKBest (ANOVA F-test) – selection of the top 20 features  
3. RandomForestClassifier – multi-class intrusion classification  

- Cross-validation: 3-fold
- Mean accuracy: ~97.5%

---

## How to Run

### 1. Preprocess the raw data
`bash
python src/01_preprocess.py


2. Train the model and evaluate performance
python src/02_train_pipeline.py

3. Run prediction on new data
python src/03_predict.py --csv path/to/input.csv --out out/predictions.csv


Results
High classification accuracy on major attack classes
Metrics per class (precision, recall, F1-score) are available in:
reports/metrics_report.txt



Conclusion
This project demonstrates a complete and reproducible NIDS machine learning pipeline, from raw data preprocessing to model training and inference.
The trained model can be reused for offline analysis or extended to real-time intrusion detection systems.
