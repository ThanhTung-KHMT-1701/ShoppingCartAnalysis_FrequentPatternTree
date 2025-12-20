# Shopping Cart Analysis

Phân tích dữ liệu bán lẻ nhằm khám phá mối quan hệ giữa các sản phẩm thường được mua cùng nhau bằng các kỹ thuật **Association Rule Mining** như **Apriori** và **FP-Growth**.  
Project triển khai pipeline đầy đủ từ xử lý dữ liệu → khai thác luật → so sánh thuật toán → trực quan hóa kết quả.

---

## Features

- Làm sạch dữ liệu & xử lý giao dịch lỗi
- Xây dựng basket matrix (transaction × product)
- Khai thác tập mục phổ biến (Frequent Itemsets)
- Sinh luật kết hợp (Association Rules)
- Hỗ trợ 2 thuật toán:
  - Apriori
  - FP-Growth
- So sánh Apriori vs FP-Growth
- Các chỉ số đánh giá:
  - Support
  - Confidence
  - Lift
- Trực quan hóa với:
  - Bar chart
  - Scatter plot
  - Network graph
  - Biểu đồ tương tác Plotly
- Tự động hóa pipeline bằng **Papermill**
- Dashboard tương tác bằng **Streamlit**

---

## Project Structure

```text
shopping_cart_advanced_analysis/
├── data/
│   ├── raw/
│   │   └── online_retail.csv
│   └── processed/
│       ├── cleaned_uk_data.csv
│       ├── basket_bool.parquet
│       ├── rules_apriori_filtered.csv
│       └── rules_fpgrowth_filtered.csv
│
├── notebooks/
│   ├── preprocessing_and_eda.ipynb
│   ├── basket_preparation.ipynb
│   ├── apriori_modelling.ipynb
│   ├── fp_growth_modelling.ipynb
│   ├── compare_apriori_fpgrowth.ipynb
│   └── runs/
│       ├── preprocessing_and_eda_run.ipynb
│       ├── basket_preparation_run.ipynb
│       ├── apriori_modelling_run.ipynb
│       ├── fp_growth_modelling_run.ipynb
│       └── compare_apriori_fpgrowth_run.ipynb
│
├── src/
│   └── apriori_library.py
│
├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── run_papermill.py
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone <your_repo_url>
cd shopping_cart_advanced_analysis
conda create -n shopping_env python=3.11
conda activate shopping_env
pip install -r requirements.txt
```

Data Preparation
Đặt file gốc tại:

```bash
data/raw/online_retail.csv
```
File output sẽ được sinh tự động vào:

```bash
data/processed/
```

Run Pipeline (Recommended)
Chạy toàn bộ phân tích chỉ với 1 lệnh:

```bash
python run_papermill.py
```
Kết quả sinh ra:

```bash
data/processed/
├── cleaned_uk_data.csv
├── basket_bool.parquet
├── rules_apriori_filtered.csv
└── rules_fpgrowth_filtered.csv

notebooks/runs/
├── preprocessing_and_eda_run.ipynb
├── basket_preparation_run.ipynb
├── apriori_modelling_run.ipynb
├── fp_growth_modelling_run.ipynb
└── compare_apriori_fpgrowth_run.ipynb
```

### Changing Parameters
Các tham số có thể chỉnh trong `run_papermill.py` hoặc trong cell `PARAMETERS` của mỗi notebook:

```python
MIN_SUPPORT=0.01
MAX_LEN=3
FILTER_MIN_CONF=0.3
FILTER_MIN_LIFT=1.2
```
Papermill cho phép chạy pipeline với cấu hình khác nhau mà không cần sửa notebook gốc.

### Visualization & Results
Các notebook modelling hiển thị các biểu đồ:

Top luật theo Lift

Top luật theo Confidence

Scatter Support – Confidence – Lift

Network graph giữa các sản phẩm

Biểu đồ Plotly tương tác

Có thể export notebook kết quả sang HTML:

```bash
jupyter nbconvert notebooks/runs/priori_modelling_run.ipynb --to html
```

### Ứng dụng thực tế
Product recommendation

Cross-selling strategy

Combo gợi ý sản phẩm

Phân tích hành vi mua hàng

Sắp xếp sản phẩm tại siêu thị

### Tech Stack

| Công nghệ | Mục đích |
|----------|----------|
| Python | Ngôn ngữ chính |
| Pandas | Xử lý dữ liệu transaction |
| MLxtend | Apriori / FP-Growth association rules |
| Papermill | Chạy pipeline notebook tự động |
| Matplotlib & Seaborn | Visualization biểu đồ tĩnh |
| Plotly | Dashboard / biểu đồ tương tác |
# Báo cáo (Tóm tắt) — Phân tích Luật Kết Hợp (Apriori & FP-Growth)

Mục tiêu: khám phá các quy tắc (association rules) giữa sản phẩm trong dataset bán lẻ "Online Retail" để rút ra insight hỗ trợ gợi ý sản phẩm, chiến lược cross-sell, và sắp xếp hàng hoá.

Ngôn ngữ: báo cáo ngắn gọn, dễ hiểu cho người không chuyên về data mining. Toàn bộ phân tích thực hiện trong thư mục `notebooks/` và mã nguồn ở `src/apriori_library.py`.

---

## 1) Bài toán & Dữ liệu
- Dữ liệu: tập giao dịch bán lẻ (invoice × item) từ file `data/raw/online_retail.csv`, đã lọc khách UK và loại bỏ giao dịch hủy. Mỗi bản ghi chứa `InvoiceNo`, `Description`, `Quantity`, `UnitPrice`, `CustomerID`, `InvoiceDate`.
- Bài toán: tìm các cặp/tập sản phẩm thường xuất hiện cùng nhau và so sánh kết quả giữa hai thuật toán phổ biến: Apriori và FP-Growth.

Tại sao quan trọng cho kinh doanh:
- Phát hiện combo bán chéo (cross-sell) và gợi ý sản phẩm.  
- Ước tính mức độ phổ biến & ảnh hưởng của mối quan hệ sản phẩm (support, confidence, lift).  

---

## 2) Pipeline (tóm tắt)
1. Tiền xử lý: làm sạch, thêm `TotalPrice`, loại bỏ hoá đơn hủy, lấy dữ liệu UK.  
2. Tạo ma trận basket (invoice × product) và mã hoá boolean (item có/không).  
3. Khai thác tập mục phổ biến: Apriori / FP-Growth (thay được tham số `min_support`, `max_len`).  
4. Sinh luật kết hợp bằng hàm `association_rules` (thông số `metric='lift'`, bộ lọc theo `confidence`).  
5. Hậu xử lý có trọng số (weighted post-processing): ghép bảng luật với bảng hoá đơn (có `TotalPrice` hoặc trọng số khách hàng) để tính `weighted_support`, `weighted_lift` — giúp phản ánh tầm quan trọng doanh thu/chi tiêu, không chỉ tần suất.

Để chạy nhanh: mở notebook `notebooks/Q2_parameter_sensitivity_analysis.ipynb` (thử nghiệm tham số), sau đó `notebooks/Q3_association_rules_visualization.ipynb` để xem trực quan và insight.

---

## 3) Kết quả chính & Insight (Tóm tắt)
- Cảm nhận chung: với ngưỡng `min_support` cao, số itemset giảm mạnh, luật có độ lift cao thường hiếm (low support) nhưng giá trị kinh doanh có thể lớn.  
- So sánh Apriori vs FP-Growth: kết quả về luật (itemsets & rules) tương tự nhau khi dùng cùng tham số; FP-Growth thường nhanh hơn trên dữ liệu lớn.  
- Weighted metrics: khi tính `weighted_support` (ví dụ trọng số = doanh thu `TotalPrice`), một vài luật ít phổ biến về mặt số lượng lại có weighted-support/lift lớn — tức là chúng ảnh hưởng nhiều tới doanh thu (ứng dụng: ưu tiên gợi ý cho chiến dịch có lợi nhuận cao hơn).

Ví dụ ngắn (hình thức minh hoạ, không dump toàn bộ bảng):

```python
# Minh hoạ ý tưởng tính weighted_support cho một rule A→B
# weight_df: bảng hóa đơn với cột 'InvoiceNo' và 'TotalPrice'
# rules: DataFrame luật với cột 'antecedents' (frozenset) và 'consequents'

def compute_weighted_support(rules, basket_df, weight_df):
    # với mỗi luật, tính tổng trọng số (TotalPrice) của các hoá đơn chứa cả antecedent và consequent
    # và chia cho tổng trọng số của tất cả hoá đơn để thu được weighted_support
    # Trả về rules với cột 'weighted_support'
    pass  # đoạn code đầy đủ có thể triển khai trong `src/apriori_library.py`
```

Ý chính: so sánh support thường và weighted_support giúp phát hiện luật "ít phổ biến nhưng có giá trị doanh thu lớn".

---

## 4) Trực quan hóa & Gợi ý đọc nhanh
- Notebook `Q2_parameter_sensitivity_analysis.ipynb`: thử nghiệm ảnh hưởng của `min_support`, `min_confidence`, `min_lift` lên số lượng itemsets, số luật, thời gian chạy và các chỉ số trung bình (avg lift, avg confidence).  
- Notebook `Q3_association_rules_visualization.ipynb`: biểu đồ scatter (support vs confidence, kích thước bubble = lift), network graph các sản phẩm, và bảng tóm tắt các luật nổi bật.

Gợi ý: đọc theo thứ tự Q2 → Q3. Q2 giúp chọn tham số hợp lý; Q3 cho insight trực quan và minh hoạ các luật đáng chú ý.

---

## 5) So sánh & Kết luận ngắn
- Apriori & FP-Growth: cùng mục tiêu, FP-Growth tiết kiệm thời gian cho dataset lớn; chọn thuật toán phụ thuộc tài nguyên và kích thước dữ liệu.  
- Các chỉ số weighted (theo doanh thu hoặc trọng số khách hàng) thường cung cấp góc nhìn thương mại hữu dụng hơn support thuần túy.  

Khuyến nghị cho thực tế: kết hợp cả hai loại luật — ưu tiên luật có weighted_lift cao khi mục tiêu là gia tăng doanh thu; ưu tiên luật có support cao khi mục tiêu là trải nghiệm khách hàng (gợi ý phổ biến).

---

## 6) Tệp liên quan & Cách chạy nhanh
- Mã: `src/apriori_library.py` (lớp `AssociationRulesMiner`, `FPGrowthMiner`).
- Notebooks chính: `notebooks/Q2_parameter_sensitivity_analysis.ipynb`, `notebooks/Q3_association_rules_visualization.ipynb`.
- Dữ liệu đầu vào: `data/raw/online_retail.csv` → kết quả vào `data/processed/`.

Để chạy toàn bộ pipeline nhanh (tại shell):

```bash
conda activate datamining
python run_papermill.py
```

---

Nếu bạn muốn, tôi có thể:
- Thêm hàm `compute_weighted_metrics` vào `src/apriori_library.py` (post-processing).  
- Chạy một ví dụ demo để xuất `rules_apriori_weighted.csv` và cập nhật notebook với hình ảnh minh hoạ.

Tác giả: Nhóm Lab — ShoppingCartAnalysis_FrequentPatternTree
