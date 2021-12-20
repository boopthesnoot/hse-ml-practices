# hse-ml-practices

* В папке *data* находятся сырые данные, предобработанные, и предсказанный результат
* В папке *notebooks*  лежит исходный jupyter-ноутбук
* В папке src лежит код проекта на python, разбитый на отдельные скрипты

Данные и код из https://www.kaggle.com/gunesevitan/titanic-advanced-feature-engineering-tutorial

Отчёт с анализом кода находится в *code_style.md*

Структура: 

```bash
├── README.md
├── Snakefile
├── code_style.md
├── data
│   ├── processed
│   │   ├── X_test.csv
│   │   ├── X_train.csv
│   │   ├── df_all.csv
│   │   ├── df_test.csv
│   │   ├── test.csv
│   │   ├── train.csv
│   │   └── y_train.csv
│   └── raw
│       ├── test.csv
│       └── train.csv
├── mkdir
├── models
│   └── rf.py
├── notebooks
│   ├── submissions.csv
│   └── titanic-advanced-feature-engineering-tutorial.ipynb
├── references
├── reports
├── src
│   ├── __init__.py
│   ├── preproc.py
│   ├── rf.py
│   └── test_prediction.py
└── workflow
    ├── __init__.py
    └── cli.py
```
