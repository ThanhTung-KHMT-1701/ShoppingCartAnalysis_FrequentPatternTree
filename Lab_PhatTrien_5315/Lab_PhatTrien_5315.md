# 📊 Lab_PhatTrien_5315: High-Utility Itemset Mining (HUIM)
## Phân tích Tập Mục Giá Trị Cao - Sự khác biệt giữa "Frequent" và "High-Utility"

**Ngày thực hiện:** 23/12/2025  
**Phương pháp:** High-Utility Itemset Mining với TWU-based Pruning và UP-Growth  
**Dữ liệu:** Online Retail UK (2010-2011)

---

## 🎯 MỤC TIÊU CỦA LAB NÀY

Theo yêu cầu của bài tập **5.3.1.5 - Cho nhóm tham vọng lấy 10: High-utility itemset mining**:

> *"Thay vì tối ưu theo số lần xuất hiện (frequent), tối ưu theo tổng "utility" (doanh thu/lợi nhuận)."*

Lab này tập trung vào:
1. **Triển khai thuật toán HUIM** - khai thác tập mục giá trị cao
2. **So sánh tư duy FIM vs HUIM** - frequent itemsets vs high-utility itemsets
3. **Phân tích ý nghĩa kinh doanh** - phát hiện những sản phẩm mà FIM truyền thống bỏ qua

---

## 💡 SỰ KHÁC BIỆT VỀ TƯ DUY: "FREQUENT" vs "HIGH-UTILITY"

### 1. Định nghĩa cơ bản

| Khái niệm | Frequent Itemset Mining (FIM) | High-Utility Itemset Mining (HUIM) |
|-----------|------------------------------|-----------------------------------|
| **Câu hỏi** | "Sản phẩm nào xuất hiện **nhiều lần** nhất?" | "Sản phẩm nào mang lại **doanh thu cao** nhất?" |
| **Metric** | Support = Frequency / Total Transactions | Utility = Σ(Quantity × UnitPrice) |
| **Giả định** | Mọi item có giá trị như nhau | Item có giá trị khác nhau |
| **Output** | Itemsets với support ≥ min_support | Itemsets với utility ≥ min_utility |

### 2. Ví dụ minh họa từ dữ liệu thực tế

#### 🔴 Trường hợp FIM phát hiện được nhưng HUIM xếp hạng thấp:

| Sản phẩm | Frequency | Rank (FIM) | Utility (£) | Rank (HUIM) | Chênh lệch |
|----------|-----------|------------|-------------|-------------|------------|
| WHITE HANGING HEART T-LIGHT HOLDER | 2,162 | **#1** | £100,497 | #4 | -3 |
| JUMBO BAG RED RETROSPOT | 1,935 | **#2** | £86,471 | #6 | -4 |
| LUNCH BAG RED RETROSPOT | 1,392 | **#5** | £29,007 | #30 | **-25** |
| LUNCH BAG BLACK SKULL | 1,216 | **#9** | £20,259 | #68 | **-59** |

**Insight**: Những sản phẩm bán chạy nhất (high frequency) không nhất thiết mang lại doanh thu cao nhất!

#### 🟢 Trường hợp HUIM phát hiện được nhưng FIM bỏ qua hoàn toàn:

| Sản phẩm | Frequency | Rank (FIM) | Utility (£) | Rank (HUIM) | Chênh lệch |
|----------|-----------|------------|-------------|-------------|------------|
| **PAPER CRAFT, LITTLE BIRDIE** | 1 | #3920 | £168,469 | **#2** | **+3918** |
| **PICNIC BASKET WICKER 60 PIECES** | 2 | #3762 | £39,619 | **#11** | **+3751** |
| **Adjust bad debt** | 1 | #3920 | £11,062 | #163 | **+3757** |
| **AMAZON FEE** | 2 | #3762 | £13,761 | #120 | **+3642** |
| MEDIUM CERAMIC TOP STORAGE JAR | 225 | #620 | £80,575 | **#7** | **+613** |

**Insight quan trọng**: 
- `PAPER CRAFT, LITTLE BIRDIE` chỉ bán **1 lần** nhưng mang lại **£168,469** (1.87% tổng doanh thu)
- FIM xếp hạng #3920 (gần cuối), nhưng HUIM xếp hạng **#2** (top đầu)
- Đây là ví dụ điển hình về **Hidden Gem** - sản phẩm có giá trị cao nhưng FIM không thể phát hiện!

### 3. Công thức so sánh

#### 📊 Frequent Itemset Mining (FIM)

$$
\text{Support}(X) = \frac{|\{T \in D : X \subseteq T\}|}{|D|}
$$

> **Giải thích**: Đếm số transaction chứa itemset $X$ chia cho tổng số transaction.
> - ✅ Đơn giản, dễ tính toán
> - ❌ Không phân biệt sản phẩm £1 và £1000

---

#### 💰 High-Utility Itemset Mining (HUIM)

**Utility của itemset $X$ trong transaction $T$:**

$$
u(X, T) = \sum_{x \in X} q(x, T) \times p(x)
$$

Trong đó:
- $q(x, T)$ = số lượng (quantity) của item $x$ trong transaction $T$
- $p(x)$ = đơn giá (unit profit) của item $x$

**Tổng Utility của itemset $X$ trong database $D$:**

$$
u(X) = \sum_{T \in D \land X \subseteq T} u(X, T)
$$

**Transaction-Weighted Utility (TWU) - Upper bound để pruning:**

$$
TWU(X) = \sum_{T \in D \land X \subseteq T} TU(T)
$$

Trong đó $TU(T) = \sum_{x \in T} q(x,T) \times p(x)$ là tổng utility của transaction $T$.

> **Tính chất quan trọng**: $TWU(X) \geq u(X)$ → Dùng để loại bỏ ứng viên sớm (pruning)

---

## 🔧 Ý TƯỞNG TRIỂN KHAI SO VỚI CÁC NOTEBOOKS CŨ

### So sánh Pipeline cũ vs mới

| Bước | Notebooks Cũ (Bước 3-5) | Lab_PhatTrien_5315 (Mới) |
|------|-------------------------|--------------------------|
| **Input** | Basket boolean (có/không mua) | Transaction với Quantity × Price |
| **Thuật toán** | Apriori, FP-Growth | TWU-based Pruning, UP-Growth |
| **Metric chính** | Support (frequency-based) | Utility (profit-based) |
| **Output** | Frequent Itemsets + Association Rules | High-Utility Itemsets |
| **Ứng dụng** | Market Basket Analysis | Revenue Optimization |

### Các thuật toán được triển khai

#### 1. TWU-based High-Utility Mining

**Transaction-Weighted Utility (TWU):**

$$
TWU(X) = \sum_{T \in D,\ X \subseteq T} TU(T)
$$

| Tính chất | Giải thích |
|-----------|------------|
| **Upper bound** | $TWU(X) \geq u(X)$ luôn đúng |
| **Anti-monotone** | Nếu $TWU(X) < \text{min\_utility}$ thì $X$ và mọi superset của $X$ đều không phải HUI |
| **Pruning** | Loại bỏ ứng viên sớm, giảm không gian tìm kiếm |

#### 2. UP-Growth (Utility Pattern Growth)

**Cải tiến của FP-Growth cho HUIM:**

| Thành phần | FP-Growth | UP-Growth |
|------------|-----------|-----------|
| Cấu trúc dữ liệu | FP-Tree | UP-Tree |
| Metric | Support count | Node utility |
| Header table | Item frequency | Item TWU |

**Các chiến lược pruning:**
- **DGU** (Discarding Global Unpromising items): Loại items có $TWU < \text{min\_utility}$
- **DGN** (Decreasing Global Node utilities): Giảm utility của node khi xây tree
- **DLU** (Discarding Local Unpromising items): Loại items không promising trong conditional pattern base
- **DLN** (Decreasing Local Node utilities): Giảm utility trong conditional UP-Tree

> **Ưu điểm**: Giảm overestimation của TWU, tìm HUI chính xác hơn

### Cấu trúc thư mục mới

```
Lab_PhatTrien_5315/
├── notebooks/
│   └── Lab_PhatTrien_5315.ipynb    # Notebook chính với HUIM
├── output/
│   ├── Case 0.5e-2 + 0.1e-2/       # Kết quả thử nghiệm
│   │   ├── SoSanh_FIM_vs_HUIM.csv  # So sánh chi tiết
│   │   ├── experiment_log.txt       # Log thử nghiệm
│   │   └── *.png, *.html            # Visualizations
│   └── ...
├── run_papermill.py                 # Script chạy automated
└── Lab_PhatTrien_5315.md            # Báo cáo này
```

---

## 📊 KẾT QUẢ THỬ NGHIỆM (Case 0.5% + 0.1%)

### Thông tin dữ liệu

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số giao dịch (dòng) | 397,924 |
| Số hoá đơn duy nhất | 18,021 |
| Số sản phẩm duy nhất | 4,007 |
| **Tổng Utility (Doanh thu)** | **£9,025,222.08** |

### Cấu hình thử nghiệm

| Tham số | Giá trị |
|---------|---------|
| Test Thresholds | 0.5% (£45,126), 0.1% (£9,025) |
| Max Itemset Length | 3 |
| Timeout per experiment | 300 giây |
| Thuật toán | TWU-based, UP-Growth |

### Kết quả chạy

| Threshold | TWU-based | UP-Growth | Ghi chú |
|-----------|-----------|-----------|---------|
| 0.5% (£45,126) | TIMEOUT (300s) | TIMEOUT (300s) | Cần threshold cao hơn |
| 0.1% (£9,025) | TIMEOUT (300s) | TIMEOUT (300s) | Cần threshold cao hơn |

**Phân tích**: Với threshold thấp (0.1-0.5%), không gian tìm kiếm quá lớn dẫn đến timeout. Điều này cho thấy cần:
- Tăng threshold lên 1-2%
- Hoặc loại bỏ outliers để giảm không gian tìm kiếm

---

## 📈 Ý NGHĨA CÁC BIỂU ĐỒ VÀ HÌNH ẢNH

### 1. Biểu đồ "3.1 Phân Tích Khả Năng Tạo K-Itemsets"
![3.1 Phan Tich Kha Nang Tao K-Itemsets.png](output/Case%200.5e-2%20+%200.1e-2/3.1%20Phan%20Tich%20Kha%20Nang%20Tao%20K-Itemsets.png)

**Ý nghĩa**: 
- Phân tích số lượng items trong mỗi hoá đơn
- Cho biết khả năng tạo 2-itemsets, 3-itemsets, 4-itemsets...
- Giúp chọn `MAX_ITEMSET_LENGTH` phù hợp để tránh lãng phí thời gian

### 2. Biểu đồ "3.2 CDF và Khuyến Nghị Threshold"
![3.2 CDF va Khuyen Nghi Threshold.png](output/Case%200.5e-2%20+%200.1e-2/3.2%20CDF%20va%20Khuyen%20Nghi%20Threshold.png)

**Ý nghĩa**:
- CDF (Cumulative Distribution Function) của utility
- Giúp chọn threshold phù hợp: threshold càng thấp → tìm được nhiều itemsets nhưng chạy lâu hơn
- Khuyến nghị: 1-2% threshold cho dataset này

### 3. Biểu đồ "3.2 Phân Bố Utility của K-Itemsets"
![3.2 Phan Bo Utility cua K-Itemsets.png](output/Case%200.5e-2%20+%200.1e-2/3.2%20Phan%20Bo%20Utility%20cua%20K-Itemsets.png)

**Ý nghĩa**:
- Phân bố utility theo độ dài itemset (1-item, 2-item, 3-item...)
- Cho thấy utility tập trung ở đâu: single items hay combinations

### 4. Biểu đồ "5.1 Runtime vs Số Lượng Itemsets"
![5.1 Runtime vs So Luong Itemsets.png](output/Case%200.5e-2%20+%200.1e-2/5.1%20Runtime%20vs%20So%20Luong%20Itemsets.png)

**Ý nghĩa**:
- Trade-off giữa thời gian chạy và số itemsets tìm được
- Threshold thấp → nhiều itemsets nhưng chạy lâu (có thể timeout)
- Threshold cao → ít itemsets nhưng chạy nhanh

### 5. Biểu đồ "7.2 So Sánh FIM vs HUIM"
![7.2 So Sanh FIM vs HUIM.png](output/Case%200.5e-2%20+%200.1e-2/7.2%20So%20Sanh%20FIM%20vs%20HUIM.png)

**Ý nghĩa**:
- **Quan trọng nhất** - So sánh trực quan ranking của FIM vs HUIM
- Điểm càng xa đường chéo → sự khác biệt giữa 2 approach càng lớn
- Các điểm ở góc trái trên: HUIM xếp hạng cao nhưng FIM xếp hạng thấp → **Hidden Gems**
- Các điểm ở góc phải dưới: FIM xếp hạng cao nhưng HUIM xếp hạng thấp → **Volume Drivers**

### 6. Ma trận "6.4 Utility-Frequency Matrix" (Interactive HTML)
**File**: `6.4 Ma Tran Utility-Frequency.html`

**Ý nghĩa**:
- Phân loại 4,007 sản phẩm thành 4 nhóm:
  - **Stars** ⭐: High Utility + High Frequency → Sản phẩm vàng
  - **Hidden Gems** 💎: High Utility + Low Frequency → HUIM phát hiện, FIM bỏ qua
  - **Volume Drivers** 📦: Low Utility + High Frequency → FIM phát hiện, HUIM đánh giá thấp
  - **Others**: Low Utility + Low Frequency → Không quan trọng

---

## 🔍 INSIGHTS

### Insight 1: HUIM phát hiện "Hidden Gems" mà FIM hoàn toàn bỏ qua

**Dữ liệu căn cứ** (từ file `SoSanh_FIM_vs_HUIM.csv`):

| Sản phẩm | Frequency | Rank FIM | Utility | Rank HUIM | Rank Δ |
|----------|-----------|----------|---------|-----------|--------|
| PAPER CRAFT, LITTLE BIRDIE | 1 | #3920 | £168,469 | #2 | **+3918** |
| PICNIC BASKET WICKER 60 PIECES | 2 | #3762 | £39,619 | #11 | **+3751** |
| MEDIUM CERAMIC TOP STORAGE JAR | 225 | #620 | £80,575 | #7 | **+613** |

**Kết luận**: 
- 5 sản phẩm Hidden Gems đóng góp **£571,373** (6.33% tổng doanh thu)
- FIM sẽ xếp những sản phẩm này gần cuối bảng (rank > 600) do tần suất thấp
- Nếu chỉ dùng FIM, doanh nghiệp sẽ **bỏ lỡ** những sản phẩm có giá trị cao này

---

### Insight 2: "Bán chạy" không có nghĩa là "sinh lời cao"

**Dữ liệu căn cứ**:

| Sản phẩm | Rank FIM | Rank HUIM | Frequency | Utility | Đánh giá |
|----------|----------|-----------|-----------|---------|----------|
| LUNCH BAG BLACK SKULL | #9 | #68 | 1,216 | £20,259 | Bán chạy nhưng lời thấp |
| NATURAL SLATE HEART CHALKBOARD | #8 | #34 | 1,219 | £27,108 | Bán chạy nhưng lời thấp |
| LUNCH BAG RED RETROSPOT | #5 | #30 | 1,392 | £29,007 | Bán chạy nhưng lời thấp |

**Kết luận**:
- 5 sản phẩm "Volume Drivers" có tổng utility chỉ **£137,732** (1.53% doanh thu)
- Nhưng chiếm **top 10** trong ranking FIM
- Nếu doanh nghiệp chỉ dựa vào FIM để quyết định đầu tư marketing/kho, sẽ đầu tư sai chỗ

---

### Insight 3: Sản phẩm "Stars" - cân bằng giữa Frequency và Utility

**Dữ liệu căn cứ**:

| Sản phẩm | Rank FIM | Rank HUIM | Frequency | Utility | Đánh giá |
|----------|----------|-----------|-----------|---------|----------|
| REGENCY CAKESTAND 3 TIER | #3 | #3 | 1,685 | £142,273 | ⭐ Perfect Star |
| WHITE HANGING HEART T-LIGHT HOLDER | #1 | #4 | 2,162 | £100,497 | ⭐ Star |
| PARTY BUNTING | #4 | #5 | 1,593 | £93,658 | ⭐ Star |
| JUMBO BAG RED RETROSPOT | #2 | #6 | 1,935 | £86,471 | ⭐ Star |
| ASSORTED COLOUR BIRD ORNAMENT | #6 | #9 | 1,371 | £54,756 | ⭐ Star |

**Kết luận**:
- 5 sản phẩm Stars đóng góp **£477,657** (5.29% doanh thu)
- Cả FIM và HUIM đều đánh giá cao những sản phẩm này
- Đây là nhóm sản phẩm lý tưởng để ưu tiên

---

### Insight 4: Outlier "PAPER CRAFT" - Cảnh báo về dữ liệu

**Dữ liệu căn cứ**:
- `PAPER CRAFT, LITTLE BIRDIE`: 1 giao dịch với Quantity = 80,995 → Utility = £168,469
- Chiếm **1.87%** tổng doanh thu từ **1 giao dịch duy nhất**

**Kết luận**:
- Đây có thể là:
  - Giao dịch B2B đặc biệt (wholesale)
  - Lỗi nhập liệu (data entry error)
  - Giao dịch cần được xem xét riêng
- HUIM phát hiện ra outlier này, trong khi FIM coi nó là sản phẩm không quan trọng (#3920)
- **Khuyến nghị**: Xem xét loại bỏ outliers (Quantity > 10,000) trước khi mining để có kết quả chính xác hơn

---

### Insight 5: Độ phức tạp của HUIM cao hơn FIM

**Dữ liệu căn cứ** (từ experiment_log.txt):
- TWU-based với threshold 0.5%: TIMEOUT sau 300s
- UP-Growth với threshold 0.5%: TIMEOUT sau 300s
- UP-Growth tạo ra 416,015 nodes trong UP-Tree (threshold 0.5%)

**Kết luận**:
- HUIM phức tạp hơn FIM vì:
  - FIM chỉ đếm frequency (binary: có/không)
  - HUIM phải tính utility cho từng item trong từng transaction
- Trade-off: HUIM cho kết quả có ý nghĩa kinh doanh hơn nhưng tốn tài nguyên hơn
- **Khuyến nghị**: Sử dụng threshold 1-2% thay vì 0.1-0.5% cho dataset lớn

---

## 📋 PHÂN LOẠI SẢN PHẨM THEO MA TRẬN UTILITY-FREQUENCY

### Thống kê tổng quan

| Category | Số sản phẩm | % | Tổng Utility | % Doanh thu |
|----------|-------------|---|--------------|-------------|
| **Stars** ⭐ | 5 | 0.12% | £477,657 | 5.29% |
| **Hidden Gems** 💎 | 5 | 0.12% | £571,373 | **6.33%** |
| **Volume Drivers** 📦 | 5 | 0.12% | £137,732 | 1.53% |
| **Others** | 3,992 | 99.64% | £7,838,459 | 86.85% |

### Chi tiết từng nhóm

#### ⭐ Stars (High Utility + High Frequency)
```
Đặc điểm: Vừa bán chạy vừa sinh lời cao → Sản phẩm vàng
Chiến lược: Duy trì stock, đầu tư marketing

1. REGENCY CAKESTAND 3 TIER       - Freq: 1,685 | Utility: £142,273
2. WHITE HANGING HEART T-LIGHT    - Freq: 2,162 | Utility: £100,497
3. PARTY BUNTING                  - Freq: 1,593 | Utility: £93,658
4. JUMBO BAG RED RETROSPOT        - Freq: 1,935 | Utility: £86,471
5. ASSORTED COLOUR BIRD ORNAMENT  - Freq: 1,371 | Utility: £54,756
```

#### 💎 Hidden Gems (High Utility + Low Frequency)
```
Đặc điểm: Ít bán nhưng sinh lời cao → FIM bỏ qua, HUIM phát hiện
Chiến lược: Tăng exposure, targeted marketing

1. DOTCOM POSTAGE                  - Freq: 706   | Utility: £206,248
2. PAPER CRAFT, LITTLE BIRDIE      - Freq: 1     | Utility: £168,469 ⚠️
3. MEDIUM CERAMIC TOP STORAGE JAR  - Freq: 225   | Utility: £80,575
4. PAPER CHAIN KIT 50'S CHRISTMAS  - Freq: 1,125 | Utility: £62,742
5. CHILLI LIGHTS                   - Freq: 650   | Utility: £53,336
```

#### 📦 Volume Drivers (Low Utility + High Frequency)
```
Đặc điểm: Bán chạy nhưng lời thấp → FIM đánh giá cao, HUIM đánh giá thấp
Chiến lược: Cân nhắc tăng giá hoặc upselling

1. HEART OF WICKER SMALL           - Freq: 1,164 | Utility: £31,394
2. SET OF 3 CAKE TINS PANTRY       - Freq: 1,241 | Utility: £29,962
3. LUNCH BAG RED RETROSPOT         - Freq: 1,392 | Utility: £29,007
4. NATURAL SLATE HEART CHALKBOARD  - Freq: 1,219 | Utility: £27,108
5. LUNCH BAG BLACK SKULL           - Freq: 1,216 | Utility: £20,259
```

---

## 🎓 KẾT LUẬN

### Tóm tắt sự khác biệt FIM vs HUIM

| Tiêu chí | Frequent Itemset Mining | High-Utility Itemset Mining |
|----------|-------------------------|----------------------------|
| **Tư duy** | "Gì xuất hiện nhiều?" | "Gì mang lại giá trị?" |
| **Metric** | Count/Frequency | Utility/Profit |
| **Ưu điểm** | Đơn giản, nhanh | Ý nghĩa kinh doanh cao |
| **Nhược điểm** | Bỏ qua giá trị | Phức tạp, tốn tài nguyên |
| **Use case** | Market basket analysis | Revenue optimization |

### Bài học rút ra

1. **FIM và HUIM bổ sung cho nhau** - không phải thay thế
2. **Hidden Gems** là phát hiện quan trọng nhất của HUIM - những sản phẩm mà FIM hoàn toàn bỏ qua
3. **Volume Drivers** cần được đánh giá lại - bán chạy không có nghĩa là sinh lời
4. **Stars** là mục tiêu lý tưởng - kết hợp ưu điểm của cả hai approach
5. **Outliers** cần được xử lý trước khi mining để có kết quả chính xác

### Hướng phát triển tiếp theo

- [ ] Chạy lại với threshold 1-2% sau khi loại bỏ outliers
- [ ] So sánh thời gian chạy TWU-based vs UP-Growth
- [ ] Tìm High-Utility 2-itemsets và 3-itemsets
- [ ] Phát triển Association Rules dựa trên High-Utility Itemsets