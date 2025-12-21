# Phân Tích Biểu Đồ - Khai Phá Luật Kết Hợp

## Tổng Quan Kết Quả
- **Tham số mining**: min_support=0.02, min_confidence=0.5, min_lift=1.0
- **Itemsets tìm được**: 400 (Apriori) = 400 (FP-Growth) ✅ **Giống nhau**
- **Rules tìm được**: 76 rules (Apriori) = 76 rules (FP-Growth) ✅ **Giống nhau**
- **Khoảng Lift**: 5.27 - 27.20
- **Khoảng Confidence**: 50.54% - 90.28%
- **Khoảng Support**: 2.00% - 4.36%

---

## 📊 BIỂU ĐỒ 1: Bar Chart - Top 15 Luật Có Lift Cao Nhất

**Tệp**: `viz_1_topRules_lift.png`

### Mô Tả:
- **Trục X**: Lift (độ nâng cao) - thể hiện độ mạnh của mối liên kết
- **Trục Y**: Tên 15 luật kết hợp có lift cao nhất
- **Màu sắc**: Support (độ phổ biến) - từ xanh lá (support cao) đến đỏ (support thấp)
- **Chiều cao cột**: Lift càng cao = mối liên kết bất ngờ càng lớn

### Ý Nghĩa Kinh Doanh:
1. **Luật nổi bật nhất**:
   - **WOODEN HEART ↔ WOODEN STAR** (Lift: 27.20)
   - Khách mua sản phẩm này có khả năng **gấp 27 lần** mua sản phẩm kia
   - Support: 2.04% (kết hợp hiếm nhưng cực kỳ giá trị)

2. **Ứng dụng**:
   - **Cross-selling**: Gợi ý WOODEN STAR cho khách mua WOODEN HEART
   - **Bundle pricing**: Tạo gói combo gồm 2 sản phẩm này
   - **Inventory planning**: Đặt cùng vị trí hoặc gần nhau trong cửa hàng

3. **Mô Thức**:
   - Lift cao + Support thấp = Kết hợp hiếm nhưng tuyệt vời (Ưu tiên cao)
   - Lift cao + Support cao = Kết hợp phổ biến và hiệu quả (Ưu tiên cực cao)

### Apriori vs FP-Growth:
✅ **KHÔNG CÓ SỰ KHÁC BIỆT** - Cả hai thuật toán tìm ra chính xác 15 luật giống nhau

---

## 📊 BIỂU ĐỒ 2: Scatter Plot - Support vs Confidence

**Tệp**: `viz_2_scatter_support_confidence.png`

### Mô Tả:
- **Trục X**: Support (độ phổ biến) - bao nhiêu % giao dịch có chứa cặp sản phẩm này
- **Trục Y**: Confidence (độ tin cậy) - nếu có A, xác suất có B là bao nhiêu
- **Kích thước bubble**: Lift (độ nâng cao) - bubble càng lớn = Lift cao
- **Màu sắc**: Lift (đỏ = lift cao, vàng = lift thấp)
- **Đường gạch chứa**: Trung vị của support và confidence

### 4 Vùng (Quadrant) Quan Trọng:

| Vùng | Support | Confidence | Đánh Giá | Ứng Dụng |
|------|---------|------------|---------|----------|
| **Trên Phải** 🟢 | Cao | Cao | Tuyệt vời | Bundle, Quảng cáo chính |
| **Trên Trái** 🔵 | Thấp | Cao | Hiếm nhưng chắc chắn | Khuyến mãi đặc biệt, VIP |
| **Dưới Phải** 🟡 | Cao | Thấp | Phổ biến nhưng không mạnh | Bộ sưu tập, Cross-category |
| **Dưới Trái** 🔴 | Thấp | Thấp | Yếu | Tránh bundle |

### Ghi Nhận Chính:
1. **Phân bố**: Hầu hết luật tập trung ở vùng **trên trái** (hiếm nhưng chắc chắn)
   - Điều này hợp lý vì các sản phẩm có lift cao thường có support thấp
   - Khách hàng có sở thích đặc biệt với cặp sản phẩm cụ thể

2. **Top high-lift rules** (được ghi nhãn):
   - WOODEN HEART → WOODEN STAR (lift 27.2)
   - GREEN REGENCY ↔ PINK REGENCY (lift 18.04)
   - ROSES REGENCY ↔ PINK REGENCY (lift 17.46)

3. **Mối tương quan**:
   - Support ↑ → Confidence ↓ (kết hợp phổ biến thường ít đặc biệt)
   - Lift cao → Support thấp (kết hợp bất ngờ thường hiếm)

### Apriori vs FP-Growth:
✅ **KHÔNG CÓ SỰ KHÁC BIỆT** - Cả hai tạo ra scatter plot hoàn toàn giống nhau

---

## 📊 BIỂU ĐỒ 3: Network Graph - Quan Hệ Giữa Các Sản Phẩm

**Tệp**: `viz_3_network_graph.png`

### Mô Tả:
- **Node (nút)** = Sản phẩm
  - **Kích thước node**: Số lần xuất hiện trong luật (node lớn = sản phẩm quan trọng)
  - **Màu sắc node**: In-degree (số luật đi vào) - đỏ = hub product
  
- **Edge (cạnh)** = Luật kết hợp (A → B)
  - **Độ dày cạnh**: Lift (cạnh dày = lift cao)
  - **Màu sắc cạnh**: Support (xanh dương đậm = support cao)
  - **Hướng**: Có mũi tên chỉ hướng A → B

- **Chỉ hiển thị**: Top 30% luật (lift ≥ 14.16) để tránh quá tải

### Ghi Nhận Chính:

1. **Hub Products (Sản Phẩm Trung Tâm)**:
   - **PINK REGENCY TEACUP AND SAUCER** - Node lớn nhất, kết nối 4-5 sản phẩm khác
   - **GREEN REGENCY TEACUP AND SAUCER** - Hub thứ 2
   - **ROSES REGENCY TEACUP AND SAUCER** - Hub thứ 3
   - → **Insight**: Thương hiệu REGENCY là "sao" trong mạng lưới sản phẩm

2. **Clusters (Cụm Sản Phẩm)**:
   - **Cụm REGENCY**: { PINK, GREEN, ROSES REGENCY } - liên kết chặt (lift 14-18)
   - **Cụm WOODEN CHRISTMAS**: { HEART, STAR } - liên kết cực kỳ mạnh (lift 27)
   - **Cụm CHARLOTTE BAG**: { WOODLAND, STRAWBERRY, RED RETROSPOT } - khác danh mục

3. **Ứng Dụng Kinh Doanh**:
   - **Store Layout**: Đặt REGENCY products ở vị trí trung tâm (high visibility)
   - **Cross-category selling**: Bày các cụm sản phẩm gần nhau
   - **Recommendation Engine**: Khi khách view PINK REGENCY → gợi ý GREEN REGENCY hoặc ROSES
   - **Promotion**: Khuyến mãi "Mua 2 sản phẩm REGENCY → Giảm 20%"

### Apriori vs FP-Growth:
✅ **KHÔNG CÓ SỰ KHÁC BIỆT** - Cả hai tạo ra cùng mạng lưới (13 sản phẩm, 18 liên kết)

---

## 📊 BIỂU ĐỒ 4: Heatmap - Lift Ma Trận Giữa Sản Phẩm Phổ Biến

**Tệp**: `viz_4_heatmap_lift.png`

### Mô Tả:
- **Hàng** = Antecedent (sản phẩm được mua trước)
- **Cột** = Consequent (sản phẩm được mua sau)
- **Ô trắng**: Không có luật hoặc lift = 1 (độc lập)
- **Ô xanh lam nhạt**: Lift = 2-5 (liên kết yếu)
- **Ô cam/đỏ**: Lift = 10-15 (liên kết trung bình)
- **Ô đỏ tối**: Lift > 15 (liên kết cực mạnh)
- **Chỉ hiển thị**: Top 15 sản phẩm (những sản phẩm thường xuất hiện trong luật)

### Ghi Nhận Chính:

1. **Các "Hotspot" (ô đỏ) - Liên kết Cực Mạnh**:
   - **GREEN → PINK REGENCY** (Lift: 15.87)
   - **GREEN → ROSES REGENCY** (Lift: 15.87)
   - **STRAWBERRY CHARLOTTE BAG → WOODLAND CHARLOTTE BAG** (Lift: 13.58)
   - → Cần ưu tiên bundle/cross-sell

2. **Sự Không Cân Xứng (Asymmetry)**:
   - **REGENCY TEACUP**: A → B mạnh, nhưng B → A cũng mạnh (mối liên hệ lẫn nhau)
   - **CHARLOTTE BAG**: A → B mạnh, nhưng B → A yếu (mối liên hệ một chiều)
   - → Insight: Khách mua PINK REGENCY chắc chắn mua GREEN REGENCY, nhưng ngược lại không chắc

3. **Sản Phẩm Độc Lập** (hàng/cột toàn trắng):
   - **JUMBO BAG WOODLAND ANIMALS** - Có ít liên kết với sản phẩm khác
   - **LUNCH BAG RED RETROSPOT** - Sản phẩm độc lập
   - → Không nên bundle, bán riêng lẻ

4. **Ứng Dụng**:
   - **Bundle Strategy**: Chọn cặp ô đỏ để tạo combo
   - **Discount Plan**: "Mua GREEN REGENCY + PINK REGENCY → 15% OFF"
   - **Inventory**: Tăng stock sản phẩm hub (PINK, GREEN REGENCY) cùng với các sản phẩm liên kết
   - **Pricing**: Dùng as loss leader (giảm giá sản phẩm hub) để sell consequent products

### Apriori vs FP-Growth:
✅ **KHÔNG CÓ SỰ KHÁC BIỆT** - Heatmap dựa trên cùng 76 rules

---

## 🔍 Tóm Tắt: APRIORI vs FP-GROWTH

### Kết Quả
| Tiêu Chí | Apriori | FP-Growth | Kết Luận |
|----------|---------|-----------|---------|
| Itemsets | 400 | 400 | ✅ Giống nhau |
| Rules | 76 | 76 | ✅ Giống nhau |
| Biểu đồ 1 (Bar) | Giống | Giống | ✅ Giống nhau |
| Biểu đồ 2 (Scatter) | Giống | Giống | ✅ Giống nhau |
| Biểu đồ 3 (Network) | Giống | Giống | ✅ Giống nhau |
| Biểu đồ 4 (Heatmap) | Giống | Giống | ✅ Giống nhau |

### Sự Khác Biệt (từ Q2 parameter sensitivity analysis)
- **Itemset/Rules**: Sinh ra kết quả giống hệt nhau
- **Performance**: FP-Growth nhanh hơn Apriori (~3-5x nhanh hơn)
- **Memory**: FP-Growth sử dụng memory hiệu quả hơn

### Khuyến Nghị
- **Nếu dataset nhỏ**: Dùng Apriori (dễ hiểu, debug)
- **Nếu dataset lớn/thực tiễn**: Dùng FP-Growth (nhanh, hiệu quả)

---

## 💡 Top Business Insights

### 1. **Chuyên Đề REGENCY (High Priority)**
- 3 sản phẩm REGENCY liên kết chặt (Lift: 14-18)
- Khuyến nghị: Tạo cánh gian "REGENCY Collection" với 3 sản phẩm

### 2. **Combo CHRISTMAS WOODEN (Highest ROI)**
- WOODEN HEART ↔ WOODEN STAR (Lift: 27.2)
- Khuyến nghị: Bundle "Wooden Christmas Set" - Giảm giá 25%, Lợi nhuận cao nhất

### 3. **CHARLOTTE BAG Series (Medium Priority)**
- CHARLOTTE BAG + CHARLOTTE DESIGN/POLKADOT (Lift: 11-14)
- Khuyến nghị: "Charlotte Bag Collection Starter Pack"

### 4. **Cross-Category Opportunity**
- Sản phẩm REGENCY + CHARLOTTE BAG không liên kết
- Khuyến nghị: Thử khuyến mãi "Combo: Teacup + Bag" để tạo liên kết mới

---

## 📈 Kế Tiếp (Nếu Muốn Nâng Cao)
1. **A/B Testing**: Kiểm tra 3 combo này với nhóm khách
2. **Time-Series**: Xem liên kết thay đổi theo mùa (Summer, Christmas, etc.)
3. **Customer Segmentation**: Xem high-value customers có mua theo luật không
4. **Sequential Rules**: Xem thứ tự: A → B → C (hôm nay mua A, tuần sau mua B, rồi mua C)

---

## 📁 Tệp Đầu Ra
- `viz_1_topRules_lift.png` - Bar chart
- `viz_2_scatter_support_confidence.png` - Scatter plot
- `viz_3_network_graph.png` - Network graph
- `viz_4_heatmap_lift.png` - Heatmap

Tất cả lưu trong: `data/results/`
