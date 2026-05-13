import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

# 1. Cấu hình Kafka Producer
# Kết nối vào Kafka Broker đang chạy trên localhost:9092
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'smart_home_data'

# 2. Hàm sinh Mock Data dựa trên Data Schema đã chốt
def generate_mock_data():
    meter_type = random.choice(['electricity', 'water'])
    
    # Tạo logic sinh ID tương ứng với loại đồng hồ
    if meter_type == 'electricity':
        meter_id = f"ELEC-{random.randint(1000, 1999)}"
        usage = round(random.uniform(0.1, 5.5), 2) # Điện: kWh
    else:
        meter_id = f"WAT-{random.randint(2000, 2999)}"
        usage = round(random.uniform(0.5, 20.0), 2) # Nước: lít/phút
        
    data = {
        "meter_id": meter_id,
        "household_id": f"HH-{random.randint(1, 1000):03d}",
        "meter_type": meter_type,
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "current_usage": usage,
        "device_status": random.choices(['OK', 'ERROR', 'LOW_BATTERY', 'SENSOR_FAULT'], weights=[0.85, 0.05, 0.05, 0.05])[0]
    }
    return data

# 3. Vòng lặp chính đẩy dữ liệu liên tục (Streaming)
if __name__ == "__main__":
    print(f"=== IOT GATEWAY ĐANG CHẠY ===")
    print(f"-> Đang kết nối tới Kafka Topic: '{TOPIC_NAME}'...")
    
    try:
        while True:
            # Sinh 1 record dữ liệu
            record = generate_mock_data()
            
            # Đẩy vào Kafka
            producer.send(TOPIC_NAME, value=record)
            
            print(f"Đã gửi: {record}")
            
            # Nghỉ 1 giây rồi gửi tiếp (mô phỏng luồng dữ liệu thời gian thực)
            time.sleep(1) 
            
    except KeyboardInterrupt:
        print("\n-> Đã nhận lệnh dừng (Ctrl+C). Đang đóng kết nối Kafka...")
    finally:
        producer.close()
        print("-> Đã ngắt kết nối an toàn.")