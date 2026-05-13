# BỐI CẢNH ĐỒ ÁN MÔN HỌC BIG DATA (KHÓA THẠC SĨ HỆ THỐNG THÔNG TIN)

## 1. Yêu cầu từ Giảng viên
Chủ đề: Big data analytics for IoT-based electricity/water meters
- A tool generating data streaming like many electricity/water meters
- Data collection: using Kafka
- Data analytics: (1) filtering, sampling, integration, (2) analytics goals – using Spark
- Visualization: using Tableau/Kibana
- Functions and performance evaluation

## 2. Mục tiêu Cốt lõi
Xây dựng một hệ thống Big Data end-to-end có khả năng: Giả lập, thu thập, xử lý thời gian thực và trực quan hóa dữ liệu từ các đồng hồ điện/nước IoT của khoảng 1000+ hộ gia đình, nhằm phát hiện các sự cố (rò rỉ, tiêu thụ bất thường, hư hỏng thiết bị).

## 3. Kiến trúc Hệ thống (Data Pipeline - Lambda/Kappa Architecture)
- Data Generation: Script Python đóng vai trò IoT Gateway, sinh dữ liệu liên tục (streaming) hoặc theo lô nhỏ (micro-batch).
- Data Collection / Ingestion: Đẩy dữ liệu vào Apache Kafka (Message Broker / Buffer).
- Data Analytics (Processing): Apache Spark (Spark Streaming/Structured Streaming) đọc data từ Kafka để:
  + Lọc dữ liệu lỗi (âm, null), chuẩn hóa, gom cụm.
  + Đặt ngưỡng cảnh báo rò rỉ nước, tiêu thụ điện tăng vọt.
- Storage: Đẩy dữ liệu đã xử lý vào Elasticsearch (truy vấn thời gian thực) và MinIO (Data Lake lưu trữ lịch sử).
- Visualization: Kết nối Kibana (hoặc Tableau) để vẽ biểu đồ Dashboards.

## 4. Lộ trình Triển khai (4 Phases)
- Phase 1: Infrastructure Setup & Data Modeling (Xây nền móng)
  Dựng môi trường Local Cluster bằng Docker. Cài đặt Kafka, Spark, MinIO, Elasticsearch, Kibana. Thiết kế Data Schema cho bản ghi điện/nước.
- Phase 2: Ingestion & Streaming Processing (Dẫn ống và lọc nước)
  Viết script Python sinh Mock data đẩy vào Kafka. Viết job Spark đọc Kafka, làm sạch, tính toán logic cảnh báo và ghi ra ES/MinIO.
- Phase 3: Data Visualization (Xây dựng mặt tiền)
  Tạo index trên Elasticsearch. Thiết kế Dashboards trên Kibana/Tableau.
- Phase 4: Performance Evaluation & Reporting (Đánh giá và Báo cáo)
  Test hiệu năng (độ trễ, thông lượng) khi tăng dữ liệu lên 10,000 - 100,000 hộ dân. Viết báo cáo.