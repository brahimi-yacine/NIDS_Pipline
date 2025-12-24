# NIDS Pipeline Project – CIC-IDS2017

## 1. Dataset Description
- Dataset Name: CIC-IDS2017  
- Source: Canadian Institute for Cybersecurity (CIC)  
- Type: Network traffic flows (CSV)  
- Objective: Intrusion detection and traffic classification  

The dataset contains both benign traffic and multiple network attacks such as DoS, DDoS, PortScan, Botnet, and more.

---

## 2. Raw Data Analysis
- Initial number of rows (flows): 2,214,469  
- Initial number of features: 79  
- File(s) loaded: combine.csv  

The raw dataset contains missing values (NaN) and infinite values (Inf), which require preprocessing before applying machine learning models.

---

## 3. Data Cleaning and Preprocessing

### 3.1 Handling Missing and Infinite Values
- Infinite values (+Inf, -Inf) were replaced by NaN  
- Rows containing NaN values were removed  
- Number of removed rows: 2,438  

### 3.2 Removal of Irrelevant Columns
The following columns were removed because they are not useful for machine learning:
- Flow ID  
- Timestamp  

### 3.3 Data Type Processing
- All feature columns were converted to numeric types  
- Non-numeric values were coerced and removed  

---

## 4. Clean Dataset Description
- Final number of rows: 2,212,030  
- Final number of features: 79 (78 input features + 1 target column: Label)  
- Target column: Label  

The cleaned dataset contains only numerical features and no missing values, making it suitable for machine learning pipelines.

---

## 5. Target Classes (Labels)
The target variable Label represents the traffic category.  

Main observed classes:

| Label             | Number of samples |
|------------------|-----------------|
| BENIGN            | 1,671,484       |
| DoS Hulk          | 230,124         |
| PortScan          | 158,804         |
| DDoS              | 128,027         |
| DoS GoldenEye     | 10,293          |
| DoS slowloris     | 5,796           |
| DoS Slowhttptest  | 5,499           |
| Bot               | 1,956           |
| Infiltration      | 36              |
| Heartbleed        | 11              |

Additional attack classes are also present, resulting in a multi-class classification problem.

---

## 6. Feature Description
- Number of input features: 78  
- Feature type: Numerical (float / integer)  

Examples of network features:
- Flow Duration  
- Total Forward Packets  
- Total Backward Packets  
- Flow Bytes/s  
- Packet Length Mean  
- Average Packet Size  

These features describe traffic behavior, packet statistics, and flow-level characteristics.

---

## 7. Machine Learning Pipeline

The cleaned dataset is used to train a Random Forest classifier using the following pipeline:

1. Feature Scaling: StandardScaler to normalize numerical features  
2. Feature Selection: SelectKBest with ANOVA F-test (f_classif) to select top 20 features  
3. Classifier: Random Forest with 200 estimators and parallel processing  

### Cross-Validation
- 5-fold cross-validation was applied to evaluate the model  
- Mean accuracy achieved: ~0.975  

### Model Training
- The final model is trained on the full cleaned dataset (all 2,212,030 rows)  
- Model and label encoder are saved in nids_pipeline.joblib  

---

## 8. Output of the Preprocessing and Training Stage
- Clean dataset: cicids_clean.csv  
- Trained model: nids_pipeline.joblib  
- The dataset and model are ready for:
  - Feature normalization  
  - Feature selection  
  - Machine learning classification  
  - Intrusion detection predictions  

---

## 9. Prediction Stage
Once trained, the pipeline can be used to predict network traffic categories on new data:

- The pipeline outputs the predicted Label for each network flow, allowing detection of malicious traffic in real-time.

---
## 10. Conclusion
- The preprocessing phase successfully transformed the raw CIC-IDS2017 dataset into a clean, structured dataset suitable for machine learning.  
- The Random Forest pipeline achieved high accuracy (~97.5%) on cross-validation.  
- The resulting model (nids_pipeline.joblib) can detect and classify multiple types of network intrusions.  
- This pipeline provides a reproducible framework for NIDS experiments and can be extended for real-time monitoring.