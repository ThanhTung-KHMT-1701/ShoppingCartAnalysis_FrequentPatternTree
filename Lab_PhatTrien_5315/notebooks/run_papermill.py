import os
from pathlib import Path

import papermill as pm

# File này nằm trong Lab_PhatTrien_5315/notebooks/
NOTEBOOKS_DIR = Path(__file__).resolve().parent
LAB_DIR = NOTEBOOKS_DIR.parent  # Lab_PhatTrien_5315/
# Project root là thư mục cha chứa data/ (ShoppingCartAnalysis_FrequentPatternTree)
PROJECT_ROOT = LAB_DIR.parent

RUNS_DIR = NOTEBOOKS_DIR / "runs"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Kiểm tra thư mục data tồn tại
if not DATA_DIR.exists():
    raise FileNotFoundError(f"❌ Không tìm thấy thư mục data tại: {DATA_DIR}")

print(f"📁 LAB_DIR: {LAB_DIR}")
print(f"📁 PROJECT_ROOT: {PROJECT_ROOT}")
print(f"📁 DATA_DIR: {DATA_DIR}")

RUNS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Chuyển working directory về PROJECT_ROOT để notebook tìm được data/
os.chdir(PROJECT_ROOT)

# Chay run_preprocessing_and_eda.py
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

# Chay run_basket_preparation.py
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
# pm.execute_notebook(
#     str(NOTEBOOKS_DIR / "compare_apriori_fpgrowth.ipynb"),
#     str(RUNS_DIR / "compare_apriori_fpgrowth_run.ipynb"),
#     parameters=dict(
#         BASKET_BOOL_PATH=str(PROCESSED_DIR / "basket_bool.parquet"),

#         MIN_SUPPORT=0.01,
#         MAX_LEN=3,

#         METRIC="lift",
#         MIN_THRESHOLD=1.0,
#     ),
#     kernel_name="python3",
# )

# =============================================================================
# Chạy Notebook High-Utility Itemset Mining (Lab_PhatTrien_5315)
# =============================================================================
pm.execute_notebook(
    str(NOTEBOOKS_DIR / "Lab_PhatTrien_5315.ipynb"),
    str(RUNS_DIR / "Lab_PhatTrien_5315_run.ipynb"),
    parameters=dict(
        # Đường dẫn dữ liệu
        CLEANED_DATA_PATH=str(PROCESSED_DIR / "cleaned_uk_data.csv"),
        OUTPUT_DIR=str(PROCESSED_DIR),
        HUI_OUTPUT_PATH=str(PROCESSED_DIR / "high_utility_itemsets.csv"),

        # Tham số tối ưu hóa
        MIN_UTILITY_PERCENT=0.1,
        MIN_UTILITY_ABSOLUTE=0,
        MAX_ITEMSET_LENGTH=2,
        
        # Timeout configuration (giây) - theo max_length
        TIMEOUT_CONFIG={
            1: 180,
            2: 300
        },

        # Tham số thử nghiệm
        # Lần 1
        # TEST_THRESHOLDS=[5e-2, 1e-2, 0.5e-2, 0.1e-2],

        # Lần 2
        TEST_THRESHOLDS=[0.01e-2, 0.005e-2, 0.0025e-2, 0.00125e-2],
        
        # Cột dữ liệu
        INVOICE_COL="InvoiceNo",
        ITEM_COL="Description",
        QUANTITY_COL="Quantity",
        PRICE_COL="UnitPrice",
        TOTAL_COL="TotalPrice",
        
        # Biểu đồ
        PLOT_TOP_HUI=True,
        PLOT_COMPARISON=True,
        PLOT_UTILITY_DISTRIBUTION=True,
        
        # Hiển thị
        TOP_N=5,
        
        # Kiểm soát chạy phân tích k-itemsets (Section 3.1, 3.2)
        RUN_ANALYSIS=True,
        
        # Màu sắc
        COLOR_BLUE='#3498db',
        COLOR_GREEN='#2ecc71',
        COLOR_ORANGE='#e67e22',
        COLOR_GRAY='#95a5a6',
        COLOR_RED='#e74c3c',
    ),
    kernel_name="python3",
)

print("✅ Đã chạy xong pipeline High-Utility Itemset Mining!")
print(f"📊 Kết quả: {RUNS_DIR / 'Lab_PhatTrien_5315_run.ipynb'}")
print(f"📁 Output: {LAB_DIR / 'output'}")
