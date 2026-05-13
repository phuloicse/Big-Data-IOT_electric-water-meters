#!/bin/bash

TOPIC_NAME=${1:-"smart_home_data"}
PARTITIONS=${2:-3}
REPLICATION_FACTOR=${3:-1}
CONTAINER_NAME="kafka-server"
BOOTSTRAP_SERVER="localhost:9092"

KAFKA_CMD="/opt/kafka/bin/kafka-topics.sh"

echo "=== KAFKA TOPIC MANAGER ==="
echo "Topic: $TOPIC_NAME | Partitions: $PARTITIONS | Replication Factor: $REPLICATION_FACTOR"

EXISTS=$(docker exec $CONTAINER_NAME $KAFKA_CMD --bootstrap-server $BOOTSTRAP_SERVER --list | grep -w "^$TOPIC_NAME$")

if [ -z "$EXISTS" ]; then
    echo "-> Trạng thái: Topic chưa tồn tại. Tiến hành tạo mới..."
    docker exec $CONTAINER_NAME $KAFKA_CMD --create \
        --bootstrap-server $BOOTSTRAP_SERVER \
        --topic $TOPIC_NAME \
        --partitions $PARTITIONS \
        --replication-factor $REPLICATION_FACTOR
    
    echo "-> Thành công: Đã tạo Topic '$TOPIC_NAME'."
else
    echo "-> Trạng thái: Topic '$TOPIC_NAME' đã tồn tại."
    echo "-> Tiến hành cập nhật số lượng Partition (Lưu ý: Chỉ áp dụng nếu số mới > số hiện tại)..."
    
    docker exec $CONTAINER_NAME $KAFKA_CMD --alter \
        --bootstrap-server $BOOTSTRAP_SERVER \
        --topic $TOPIC_NAME \
        --partitions $PARTITIONS
        
    echo "-> Hoàn tất quá trình cập nhật."
fi
echo "==========================="