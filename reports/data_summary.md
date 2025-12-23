# Data Summary – CIC-IDS2017
## Projet 3.1 – NIDS Pipeline (Machine Learning)

---

## 1. Dataset Description

- Dataset name: CIC-IDS2017  
- Source: Canadian Institute for Cybersecurity (CIC)  
- Type: Network traffic flows (CSV)  
- Objective: Intrusion detection and traffic classification  

The dataset contains both benign traffic and multiple network attacks such as DoS, DDoS, PortScan, Botnet, etc.

---

## 2. Raw Data Analysis

- Initial number of rows (flows): 2,214,469  
- Initial number of features: 79  
- File(s) loaded: combine.csv  

The raw dataset contains missing values (NaN) and infinite values (Inf), which require preprocessing before machine learning.

---

## 3. Data Cleaning and Preprocessing

The following preprocessing steps were applied:

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
- Final number of features: 79  
- Target column: Label  

The cleaned dataset contains only numerical features and no missing values, making it suitable for machine learning pipelines.

---

## 5. Target Classes (Labels)

The target variable Label represents the traffic category.

Main observed classes:

| Label       | Number of samples |
|------------|-------------------|
| BENIGN     | 1,671,484 |
| DoS Hulk  | 230,124 |
| PortScan  | 158,804 |

Additional attack classes are also present (Bot, DDoS, Slowloris, GoldenEye, etc.), resulting in a multi-class classification problem.

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

## 7. Output of the Preprocessing Stage

The preprocessing stage produces the following output:

- Clean dataset: cicids_clean.csv
- Ready for:
  - Feature normalization
  - Feature selection
  - Machine learning classification

This dataset serves as the input for the next stages of the NIDS pipeline (training, evaluation, and deployment).

---

## 8. Conclusion

The preprocessing phase successfully transformed the raw CIC-IDS2017 dataset into a clean and structured dataset suitable for machine learning.  
All data quality issues were addressed, and the resulting dataset ensures reliable and reproducible intrusion detection experiments.

