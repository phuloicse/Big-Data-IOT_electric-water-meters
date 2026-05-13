# Kế hoạch Triển khai Dự án Big Data - IoT: Hệ thống Đồng hồ Điện & Nước

## Phase 1: Xây nền móng (Infrastructure Setup & Data Modeling)
* **Thiết kế Data Schema:** Xây dựng cấu trúc dữ liệu chi tiết cho các bản ghi đồng hồ điện/nước nhằm tối ưu hóa việc lưu trữ và truy vấn.
* **Thiết lập môi trường Local Cluster:** Sử dụng Docker Compose để triển khai hạ tầng.
* **Hệ thống hạ tầng (7 dịch vụ chính):**
    * **Kafka:** Hoạt động ở chế độ KRaft (không cần Zookeeper).
    * **Kafka UI:** Giao diện quản lý và giám sát các luồng dữ liệu (topics).
    * **Spark Master & Spark Worker:** Hệ thống xử lý dữ liệu phân tán.
    * **Elasticsearch:** Công cụ lưu trữ và tìm kiếm dữ liệu tốc độ cao.
    * **Kibana:** Nền tảng trực quan hóa dữ liệu từ Elasticsearch.
    * **MinIO:** Lưu trữ đối tượng (Object Storage) cho dữ liệu thô hoặc kết quả xử lý lâu dài.

## Phase 2: Dẫn ống và lọc nước (Ingestion & Streaming Processing)
* **Phát sinh dữ liệu (Mock Data):** Triển khai script Python để mô phỏng dữ liệu thực tế từ các thiết bị IoT và đẩy vào Kafka.
* **Xử lý luồng với Spark:**
    * Viết các Spark Jobs để tiêu thụ dữ liệu từ Kafka.
    * Thực hiện làm sạch dữ liệu (Data Cleaning).
    * Tính toán logic cho các kịch bản cảnh báo (Alerting).
    * Ghi kết quả đầu ra đồng thời vào **Elasticsearch** (để hiển thị) và **MinIO** (để lưu trữ).

## Phase 3: Xây dựng mặt tiền (Data Visualization)
* **Quản lý Index:** Tạo và cấu hình các index tương ứng trên Elasticsearch để tối ưu hiệu suất lưu trữ.
* **Thiết kế Dashboard:** Sử dụng **Kibana** (hoặc Tableau) để xây dựng các biểu đồ trực quan, theo dõi chỉ số tiêu thụ và trạng thái cảnh báo theo thời gian thực.

## Phase 4: Đánh giá và Báo cáo (Performance Evaluation & Reporting)
* **Kiểm thử hiệu năng:** Đánh giá độ trễ (latency) và thông lượng (throughput) của toàn bộ hệ thống.
* **Mô phỏng quy mô lớn:** Thực hiện test với khối lượng dữ liệu từ 10.000 đến 100.000 hộ dân để đánh giá khả năng mở rộng.
* **Nghiệm thu:** Viết báo cáo đánh giá chi tiết và hoàn tất hồ sơ đồ án.