import os
from pathlib import Path

import papermill as pm

LAB_DIR = Path(__file__).resolve().parent
# Workspace root is expected to contain the shared `data/` directory.
PROJECT_ROOT = LAB_DIR.parent if (LAB_DIR.parent / "data").exists() else LAB_DIR

NOTEBOOKS_DIR = LAB_DIR / "notebooks"
RUNS_DIR = NOTEBOOKS_DIR / "runs"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RUNS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Ensure relative imports/paths inside notebooks resolve against this Lab folder.
os.chdir(LAB_DIR)

# run_preprocessing_and_eda.py
# pm.execute_notebook(
#     str(NOTEBOOKS_DIR / "preprocessing_and_eda.ipynb"),
#     str(RUNS_DIR / "preprocessing_and_eda_run.ipynb"),
#     parameters=dict(
#         DATA_PATH=str(RAW_DIR / "online_retail.csv"),
#         COUNTRY="United Kingdom",
#         OUTPUT_DIR=str(PROCESSED_DIR),
#         PLOT_REVENUE=True,         # tắt bớt plot khi chạy batch
#         PLOT_TIME_PATTERNS=True,
#         PLOT_PRODUCTS=True,
#         PLOT_CUSTOMERS=True,
#         PLOT_RFM=True,
#     ),
#     kernel_name="python3",
# )

# run_basket_preparation.py

# pm.execute_notebook(
#     str(NOTEBOOKS_DIR / "basket_preparation.ipynb"),
#     str(RUNS_DIR / "basket_preparation_run.ipynb"),
#     parameters=dict(
#         CLEANED_DATA_PATH=str(PROCESSED_DIR / "cleaned_uk_data.csv"),
#         BASKET_BOOL_PATH=str(PROCESSED_DIR / "basket_bool.parquet"),
#         INVOICE_COL="InvoiceNo",
#         ITEM_COL="Description",
#         QUANTITY_COL="Quantity",
#         THRESHOLD=1,
#     ),
#     kernel_name="python3",
# )

# Chạy Notebook Apriori Modelling
# pm.execute_notebook(
#     str(NOTEBOOKS_DIR / "apriori_modelling.ipynb"),
#     str(RUNS_DIR / "apriori_modelling_run.ipynb"),
#     parameters=dict(
#         BASKET_BOOL_PATH=str(PROCESSED_DIR / "basket_bool.parquet"),
#         RULES_OUTPUT_PATH=str(PROCESSED_DIR / "rules_apriori_filtered.csv"),

#         # Tham số Apriori
#         MIN_SUPPORT=0.01,
#         MAX_LEN=2,

#         # Generate rules
#         METRIC="lift",
#         MIN_THRESHOLD=1.0,

#         # Lọc luật
#         FILTER_MIN_SUPPORT=0.01,
#         FILTER_MIN_CONF=0.3,
#         FILTER_MIN_LIFT=1.2,
#         FILTER_MAX_ANTECEDENTS=2,
#         FILTER_MAX_CONSEQUENTS=1,

#         # Số luật để vẽ
#         TOP_N_RULES=5,

#         # Tắt plot khi chạy batch (bật = True nếu muốn xem hình)
#         PLOT_TOP_LIFT=True,
#         PLOT_TOP_CONF=True,
#         PLOT_SCATTER=True,
#         PLOT_NETWORK=True,
#         PLOT_PLOTLY_NETWORK=True,
#         PLOT_PLOTLY_SCATTER=True,  
#     ),
#     kernel_name="python3",
# )

# Chạy Notebook FP_Growth Modelling
# pm.execute_notebook(
#     str(NOTEBOOKS_DIR / "fp_growth_modelling.ipynb"),
#     str(RUNS_DIR / "fp_growth_modelling_run.ipynb"),
#     parameters=dict(
#         BASKET_BOOL_PATH=str(PROCESSED_DIR / "basket_bool.parquet"),
#         RULES_OUTPUT_PATH=str(PROCESSED_DIR / "rules_fpgrowth_filtered.csv"),

#         MIN_SUPPORT=0.01,
#         MAX_LEN=3,

#         METRIC="lift",
#         MIN_THRESHOLD=1.0,

#         FILTER_MIN_SUPPORT=0.01,
#         FILTER_MIN_CONF=0.3,
#         FILTER_MIN_LIFT=1.2,
#         FILTER_MAX_ANTECEDENTS=2,
#         FILTER_MAX_CONSEQUENTS=1,

#         TOP_N_RULES=5,

#         PLOT_TOP_LIFT=True,
#         PLOT_TOP_CONF=True,
#         PLOT_SCATTER=True,
#         PLOT_NETWORK=True,
#         PLOT_PLOTLY_SCATTER=True,
#     ),
#     kernel_name="python3",
# )

# Chạy Notebook So sánh Apriori và FP-Growth
pm.execute_notebook(
    str(NOTEBOOKS_DIR / "compare_apriori_fpgrowth.ipynb"),
    str(RUNS_DIR / "compare_apriori_fpgrowth_run.ipynb"),
    parameters=dict(
        BASKET_BOOL_PATH=str(PROCESSED_DIR / "basket_bool.parquet"),

        MIN_SUPPORT=0.01,
        MAX_LEN=3,

        METRIC="lift",
        MIN_THRESHOLD=1.0,
    ),
    kernel_name="python3",
)

print("Đã chạy xong pipeline")
