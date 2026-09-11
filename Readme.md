# RFM -Customer Segmentation

## 1. Description
Segmentscustomer by purchase pattern taking into account RFM (Recency, Frequency, Monetary Value) with K-Means (k=3) to identify churn and core customers.

## Project Structure:

```md
Market_Basket_Analysis/
├── .vscode/                   # VS Code settings
│   ├── extensions.json
│   └── settings.json
├── ***files/***                # Data files
│   └── sales.parquet           # Processed data (anymous)
├── data/                       # processing data
│   ├── demo.ipynb              # A jupyter notebook to test the model
│   ├── clustering_rfm_model.pkl# the model itself  (it will be the output of Training.ipynb)
│   └── clean.py                # Data cleaning script
├── __init__.py                 # Python package marker
├── .gitignore                  # Ignored files
└── Readme.md                   # Project documentation

```

---

## Instalations

python -m venv .venv

**For windows** -> source -venv/Scripts/activate
**For Linux** -> source -venv/bin/activate

pip install -r requirements.txt


## Usage 
1. go to ***Training.ipynb*** process and execute all the cells, there you are going to be able to whole process of training
2. After you exetuce it all, yu'll receive the model it trained to predict the new customers and relocate the old ones you have
3. Try it out in **demo.ipynb** 

---

## Methodology
1. Filter `montoventapesos>0`
2. Scaling process: ``ColumnTranformer(MinMax + QuantileTransformer) + transformer_weights`
3. Clustering: `KMeans(k=3, random_State=42)`
4. Labeling: median per cluster -> `core / leaving / totally_inactives`

--- 
## Visualization
[Click here to see the Power BI visualization](https://app.powerbi.com/view?r=eyJrIjoiNmY4MjczMDctMWQ4ZC00YzZlLWExYTQtYjRiZmNkZDQyMDdlIiwidCI6IjM4NTVmZDBlLTJlOWEtNGZjYy05NTUyLTg3OGEwZmU0YTA1ZCIsImMiOjR9)

