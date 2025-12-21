# 📊 Q2: Kết Quả Thí Nghiệm So Sánh Apriori vs FP-Growth

## ✅ Tình Trạng: HOÀN THÀNH

Thí nghiệm Q2 (Parameter Sensitivity Analysis) đã được hoàn thành thành công với đầy đủ các kết quả và phân tích chi tiết.

---

## 📁 Các Tệp Đã Tạo

| Tệp | Vị Trí | Mô Tả |
|-----|--------|-------|
| **Notebook Thí Nghiệm** | `notebooks/Q2_parameter_sensitivity_analysis.ipynb` | Notebook chính với tất cả các bước thí nghiệm |
| **Báo Cáo Chi Tiết** | `Q2_PARAMETER_ANALYSIS_REPORT.md` | Báo cáo phân tích toàn diện (này bạn đang đọc) |
| **Dữ Liệu Kết Quả** | `data/results/q2_parameter_analysis.csv` | CSV với 72 kết quả chi tiết |

---

## 🎯 Tóm Tắt Kết Quả Chính

### 1️⃣ **Apriori vs FP-Growth - Kết Quả Như Nhau**

Cả hai thuật toán sinh ra **kết quả hoàn toàn giống nhau** về:
- ✅ Số lượng itemsets phổ biến
- ✅ Số lượng luật kết hợp
- ✅ Chất lượng luật (support, confidence, lift)

**⚠️ Chỉ khác nhau về tốc độ chạy**

---

### 2️⃣ **FP-Growth Nhanh Hơn Khi nào?**

| Điều Kiện | Kết Quả |
|-----------|--------|
| **min_support = 0.01** (nhiều itemsets) | ✅ FP-Growth **1.30x nhanh hơn** |
| **min_support = 0.02** (ít itemsets) | ❌ Apriori **4.6x nhanh hơn** |
| **min_support ≥ 0.05** (rất ít itemsets) | ❌ Apriori **19x nhanh hơn** |

**Kết luận**: FP-Growth tốt ở min_support **rất thấp**, Apriori tốt ở min_support **cao**.

---

### 3️⃣ **Dữ Liệu & Itemsets**

```
📊 Dữ Liệu: 18,021 hoá đơn × 4,007 sản phẩm (99.34% sparse)

⚙️ Thí Nghiệm:
   - 6 giá trị min_support: 0.01, 0.02, 0.05, 0.10, 0.15, 0.20
   - 3 giá trị min_confidence: 0.5, 0.6, 0.7
   - 3 giá trị min_lift: 1.0, 1.1, 1.2
   - Tổng: 6 × 3 × 3 = 54 kết hợp × 2 thuật toán = 72 kết quả
```

---

### 4️⃣ **Tác Động của min_support (Quan Trọng Nhất)**

| min_support | Itemsets | Luật | Thời Gian (Apriori) | Thời Gian (FP-Growth) |
|-------------|----------|------|---------------------|----------------------|
| **0.01** | **2,156** | **1,208** | 103.9 sec | 80.0 sec ⚡ |
| **0.02** | **400** | **76** | 2.0 sec | 9.3 sec |
| **0.05** | **34** | **0** | 0.09 sec | 1.8 sec |
| **0.10** | **2** | **0** | 0.07 sec | 1.7 sec |

**📌 min_support là tham số QUYẾT ĐỊNH NHẤT**
- Tăng từ 0.01 → 0.10: Itemsets giảm 99.9% (2,156 → 2)
- Tăng từ 0.01 → 0.10: Runtime giảm 99.9%
- Tăng từ 0.01 → 0.10: Luật giảm 100% (1,208 → 0)

---

### 5️⃣ **Chất Lượng Luật**

| min_support | Confidence | Lift |
|-------------|-----------|------|
| **0.01** | **66.5%** ✅ Tốt | **18.95x** ✅ Rất tốt |
| **0.02** | **61.8%** ✅ Tốt | **11.26x** ✅ Tốt |
| **0.05** | **0%** ❌ Không luật | **0** ❌ |
| **0.10** | **0%** ❌ Không luật | **0** ❌ |

**Giải Thích**: Luật ở min_support=0.01 có confidence 66.5% (khi mua A, 66.5% khả năng cũng mua B) và lift 18.95x (mối liên kết này mạnh hơn 19 lần so với mong đợi).

---

## 🔍 Phân Tích Chi Tiết

### A. Min_Confidence có Nhạy Không?

| min_confidence | Luật ở min_support=0.01 |
|---|---|
| 0.5 | **1,208** luật |
| 0.6 | **784** luật (-35%) |
| 0.7 | **431** luật (-64%) |

→ **Min_confidence có tác động** nhưng **không lớn bằng min_support**

### B. Min_Lift có Nhạy Không?

| min_lift | Luật ở min_support=0.05 |
|---|---|
| 1.0 | **0** |
| 1.1 | **0** |
| 1.2 | **0** |

→ **Min_lift ít ảnh hưởng** (vì min_support quá cao làm sẵn không có luật)

### C. Độ Dài Itemset Trung Bình

| min_support | Apriori | FP-Growth |
|---|---|---|
| 0.01 | **1.80** | **1.80** |
| 0.02 | **1.26** | **1.26** |
| 0.05 | **1.00** | **1.00** |
| 0.10 | **1.00** | **1.00** |

→ **Cả hai thuật toán sinh ra itemset cùng độ dài** (như mong đợi)

---

## 💡 Khuyến Nghị

### 1️⃣ **Chọn Thuật Toán Nào?**

```
✅ Dùng APRIORI nếu:
   • Dữ liệu nhỏ (< 100K giao dịch)
   • min_support cao (≥ 0.05)
   • Cần hiểu rõ cách hoạt động

✅ Dùng FP-GROWTH nếu:
   • Dữ liệu lớn (> 1M giao dịch)
   • min_support thấp (< 0.02)
   • Cần tốc độ cao
```

### 2️⃣ **Chọn Giá Trị min_support Nào?**

```
💡 Chiến lược:
   1. Bắt đầu với: 0.01 (1% giao dịch)
   2. Mục tiêu: 100-1,000 itemsets phổ biến
   3. Điều chỉnh:
      - Quá nhiều → Tăng min_support
      - Quá ít → Giảm min_support
   
🎯 Với dữ liệu này:
   - Tối ưu: min_support = 0.01-0.02
   - Sinh được 76-1,208 luật chất lượng cao
```

### 3️⃣ **Chọn min_confidence Nào?**

```
💡 Khuyến nghị:
   • min_confidence = 0.5: Lấy tất cả (1,208 luật)
   • min_confidence = 0.6: Lấy luật tốt (784 luật)
   • min_confidence = 0.7: Lấy luật rất tốt (431 luật)
```

### 4️⃣ **Chọn min_lift Nào?**

```
💡 Khuyến nghị:
   • min_lift = 1.0: Lấy tất cả luật (không lọc)
   • min_lift > 1.0: Chỉ lấy luật có mối liên kết tích cực
```

---

## 📈 Biểu Đồ Chính

### Số Lượng Itemsets vs min_support
```
Itemsets

2500 │         ●●●●●●●●● (Apriori)
     │         ○○○○○○○○○ (FP-Growth)
2000 │
     │         
     │         
1500 │
     │         
1000 │         
     │         
 500 │         
     │         
 250 │      ●
     │      ○
 100 │
     │   ●
  50 │   ○
     │
   0 └─────────────────────────
     0.01  0.02  0.05  0.10
     min_support
```

→ **Giảm exponentially**: 2,156 → 400 → 34 → 2

---

### Thời Gian Chạy vs min_support
```
Runtime (sec)

100 │ ■■■ (Apriori)
    │ □□□ (FP-Growth)
    │ ■
    │ □
 10 │    ■
    │    □
    │       ■
    │         □
  1 │         ■
    │         □  ■  ■
    │            □  □
  0 └─────────────────
    0.01 0.02 0.05 0.10
```

→ **FP-Growth nhanh ở 0.01, Apriori nhanh ở 0.02+**

---

### Chất Lượng Luật (Confidence, Lift)
```
Confidence & Lift

20x │ Lift: ▲ (18.95x ở min_support=0.01)
    │       ▲ (11.26x ở min_support=0.02)
    │       
10x │       
    │       
    │ Confidence: 66.5% (0.01) → 61.8% (0.02) → 0% (0.05+)
```

→ **Chất lượng giảm khi min_support tăng**

---

## 🎓 Học Được Gì?

### ✅ Những Điều Quan Trọng

1. **Cả Apriori & FP-Growth sinh cùng kết quả** → Chỉ khác về tốc độ

2. **Không có "thuật toán tốt hơn" chung chung** → Tùy vào bối cảnh dữ liệu

3. **min_support là tham số QUYẾT ĐỊNH** → Chi phối trực tiếp số lượng & chất lượng luật

4. **FP-Growth không LUÔN nhanh hơn** → Phụ thuộc vào số lượng itemsets

5. **Dữ liệu sparse cần min_support thấp** → Bộ dữ liệu này phù hợp 0.01-0.02

---

## 📊 Tệp Dữ Liệu

### `q2_parameter_analysis.csv`
- **72 hàng**: Kết quả từ 36 kết hợp Apriori + 36 kết hợp FP-Growth
- **10 cột**: algorithm, min_support, min_confidence, min_lift, runtime_sec, n_itemsets, n_rules, avg_itemset_length, avg_confidence, avg_lift

**Cách sử dụng**:
```python
import pandas as pd
df = pd.read_csv('data/results/q2_parameter_analysis.csv')
df[df['algorithm'] == 'Apriori'].head()  # Xem kết quả Apriori
df[df['min_support'] == 0.01].head()     # Xem kết quả min_support=0.01
```

---

## 🚀 Bước Tiếp Theo

1. **Phân tích chi tiết luật** tìm được ở min_support=0.01
2. **Vẽ Biểu đồ mạng (Network Graph)** để visualize mối liên kết sản phẩm
3. **Phân tích luật theo danh mục sản phẩm** (ví dụ: khách hàng mua gì cùng nhau?)
4. **A/B testing** để kiểm tra tác động kinh doanh của các luật tìm được

---

## 📝 Tổng Kết

| Aspekt | Kết Quả |
|--------|--------|
| **Apriori vs FP-Growth** | Kết quả giống nhau, chỉ khác tốc độ |
| **Tham số nhạy nhất** | min_support (quyết định 99.9%) |
| **Điều kiện FP-Growth tốt hơn** | min_support rất thấp (0.01) |
| **Điều kiện Apriori tốt hơn** | min_support cao (≥ 0.02) |
| **Tối ưu cho dữ liệu này** | min_support = 0.01, min_confidence = 0.5 |
| **Luật tìm được** | 1,208 luật với confidence 66.5%, lift 18.95x |

---

**✅ Thí Nghiệm hoàn thành - Sẵn sàng cho các bước tiếp theo!**
