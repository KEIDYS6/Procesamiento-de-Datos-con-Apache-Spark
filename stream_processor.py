from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, window, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'beneficios_stream'
APP_NAME = 'TareaBigData_SparkStreaming'

json_schema = StructType([
    StructField("timestamp", IntegerType()),
    StructField("departamento", StringType()),
    StructField("etnia", StringType()),
    StructField("edad_min", IntegerType()),
    StructField("monto_beneficio", IntegerType())
])

def main():
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    print("\n--- INICIO PROCESAMIENTO STREAMING: KAFKA ---")
    df_stream = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()
    df_raw = df_stream.selectExpr("CAST(value AS STRING) as json_payload", "timestamp as processing_time")
    df_parsed = df_raw.withColumn(
        "data", from_json(col("json_payload"), json_schema)
    ).select(
        (col("data.timestamp").cast(TimestampType())).alias("event_time"),
        col("data.departamento"),
        col("data.etnia"),
        col("data.monto_beneficio")
    )
    df_analysis = df_parsed.withWatermark("event_time", "1 minute") \
        .groupBy(window(col("event_time"), "10 seconds").alias("window"), col("etnia")) \
        .agg(count("*").alias("conteo_eventos"), avg(col("monto_beneficio")).alias("monto_promedio"))
    query = df_analysis.writeStream.outputMode("update").format("console").option("truncate", "false").start()
    print(f"Spark Streaming escuchando en {KAFKA_TOPIC}. Presiona Ctrl+C para detener.")
    query.awaitTermination()

if __name__ == "__main__":
    main()
