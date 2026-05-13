# DATA MODEL (MÔ HÌNH DỮ LIỆU)

Mô hình dữ liệu được thiết kế dưới dạng JSON để mô phỏng bản ghi từ các đồng hồ điện/nước IoT. Dữ liệu này sẽ được stream liên tục về hệ thống.

## 1. Mẫu JSON Data (Ví dụ)

{
  "meter_id": "ELEC-1045",
  "household_id": "HH-089",
  "meter_type": "electricity",
  "timestamp": "2026-05-13T13:58:15Z",
  "current_usage": 15.4,
  "device_status": "OK"
}

## 2. Chi tiết các trường dữ liệu (Fields)

* **`meter_id` (String):** * **Mô tả:** Định danh duy nhất cho từng thiết bị đo lường.
  * [cite_start]**Mục tiêu:** Dùng để theo dõi và phân biệt dữ liệu của hơn 1000 thiết bị khác nhau trong hệ thống.
* **`household_id` (String):**
  * **Mô tả:** Định danh của hộ gia đình sở hữu đồng hồ đó.
  * [cite_start]**Mục tiêu:** Phục vụ cho bước Data Analytics bằng Apache Spark để "gom cụm" (clustering) dữ liệu theo từng hộ dân hoặc khu vực, từ đó tính toán tổng lượng tiêu dùng hoặc đối chiếu hóa đơn.
* **`meter_type` (String):**
  * **Mô tả:** Phân loại thiết bị là electricity (điện) hay water (nước).
  * [cite_start]**Mục tiêu:** Giúp Spark áp dụng đúng logic phân tích và ngưỡng cảnh báo tương ứng (ví dụ: ngưỡng cảnh báo rò rỉ nước sẽ khác với ngưỡng tiêu thụ điện tăng vọt).
* **`timestamp` (Datetime/String):**
  * [cite_start]**Mô tả:** Thời điểm chính xác mà thiết bị IoT ghi nhận số liệu.
  * **Mục tiêu:** Đây là trường quan trọng nhất trong xử lý luồng (Streaming Processing), giúp hệ thống nhận diện dữ liệu thời gian thực và vẽ biểu đồ chuỗi thời gian (time-series) trên Kibana.
* **`current_usage` (Float):**
  * [cite_start]**Mô tả:** Chỉ số tiêu thụ hiện tại (ví dụ: kWh đối với điện, m³ hoặc lít đối với nước).
  * **Mục tiêu:** Là chỉ số cốt lõi để Spark kiểm tra xem có vượt "ngưỡng cảnh báo" hay không, đồng thời dùng để lọc các dữ liệu lỗi như giá trị âm hoặc null.
* **`device_status` (String):**
  * [cite_start]**Mô tả:** Mã trạng thái của phần cứng (ví dụ: OK, ERROR, LOW_BATTERY, SENSOR_FAULT).
  * **Mục tiêu:** Đáp ứng trực tiếp bài toán kinh doanh về việc phát hiện "hư hỏng thiết bị" và hỗ trợ bảo trì dự đoán (Predictive Maintenance).