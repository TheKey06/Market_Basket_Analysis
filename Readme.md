# Forecasting project

I started this project to evaluate which group of clients, who share the same statistics, will probable buy a different product.

I just began this journey, so **Let's go**


***First:*** To get the data you have to go to my drive, I will add the link below, extract the files and put the directory with the files in the root of the project, with this structure:

**link:** https://drive.google.com/file/d/1k-K2RHWPMhSlEPwrGnhedrNO6602ivII/view?usp=sharing

Structure:
```python
Market_Basket_Analysis/
├── .vscode/                   # VS Code settings
│   ├── extensions.json
│   └── settings.json
├── ***files/***                     # Data files
│   ├── diario.parquet          # Daily sales data
│   └── sales.parquet           # Processed data
├── notebooks/                   # Jupyter notebooks
│   └── clean.ipynb             # Data cleaning notebook
├── __init__.py                  # Python package marker
├── .gitignore                   # Ignored files
└── Readme.md                    # Project documentation

```

---

## Cleaning data

The notebook called **clean** has the way we clean the documents, in this ocasion there is a rule the company is aplying, due to, every product has some initials, and those mean to the brand that they belong to, and to clean the data that is very juicy because I took all the rerefences calling their brand, group, line and even its name (_because some of them didn't have the name_), everything mean the process the data in the best way.


---
***Notes:*** In my case I am using 2 Operation System, Linux and Windows, so in the folder .vscode I configured the selectect interpreter due to I created a virtual enviroment just to not having problemsn with my dependencies, so there will be a line called:

### *this case will be applied if you use windows:*
```python
"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe"
```

### *this case will be applied if you use **Linux**:*
```python
"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\bin\\python.exe"
```
