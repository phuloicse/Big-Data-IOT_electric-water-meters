import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark_version = pyspark.__version__
scala_version = "2.13" if spark_version.startswith("4") else "2.12"

# --- BẢN VÁ LỖI: Đồng bộ thư viện AWS S3 với chính xác phiên bản Hadoop 3.4.2 của Spark 4 ---
kafka_pkg = f"org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}"
minio_pkgs = "org.apache.hadoop:hadoop-aws:3.4.2,com.amazonaws:aws-java-sdk-bundle:1.12.367"
packages = f"{kafka_pkg},{minio_pkgs}"

print(f"=== ĐANG KHỞI ĐỘNG SPARK {spark_version} (Scala {scala_version}) ===")

# Khởi tạo SparkSession với cấu hình bảo mật chuẩn SDK v2
spark = SparkSession.builder \
    .appName("SmartHomeStreaming") \
    .master("local[*]") \
    .config("spark.jars.packages", packages) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.endpoint.region", "us-east-1") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schema dữ liệu
schema = StructType([
    StructField("meter_id", StringType(), True),
    StructField("household_id", StringType(), True),
    StructField("meter_type", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("current_usage", DoubleType(), True),
    StructField("device_status", StringType(), True)
])

print("-> Đang kết nối tới Kafka topic 'smart_home_data'...")
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "smart_home_data") \
    .option("startingOffsets", "latest") \
    .load()

parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Lọc bỏ các bản ghi bị lỗi kỹ thuật (chỉ số đo < 0)
cleaned_df = parsed_df.filter(col("current_usage") >= 0)

print(f"-> Đang ghi dữ liệu chuẩn hóa xuống MinIO bucket 'iot-data-lake'...")

query_console = cleaned_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query_minio = cleaned_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3a://iot-data-lake/smart_home_data/") \
    .option("checkpointLocation", "s3a://iot-data-lake/checkpoints/") \
    .start()

spark.streams.awaitAnyTermination()