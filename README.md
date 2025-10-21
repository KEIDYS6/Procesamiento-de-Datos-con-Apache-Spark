# 🚀 Proyecto Big Data Colombia 🇨🇴

Procesamiento **Batch** y **Streaming en Tiempo Real** usando **PySpark**, **Hadoop** y **Kafka**.  
Este proyecto permite limpiar, transformar y analizar datos sobre beneficios sociales en Colombia, tanto en modo batch (por lotes) como en tiempo real con Kafka.

## 🗂️ Estructura del Proyecto

```
bigdata_colombia_project/
├── batch_processor.py
├── producer.py
├── stream_processor.py
├── requirements.txt
└── README.md
```

## ⚙️ Requisitos Previos

Instala las librerías necesarias en Python:

```bash
pip install pyspark kafka-python
```

## 🧩 Procesamiento Batch

```bash
start-dfs.sh
start-yarn.sh
wget -O datos_colombia.csv https://www.datos.gov.co/api/views/xfif-myr2/rows.csv?accessType=DOWNLOAD
hdfs dfs -mkdir -p /user/hadoop/tarea_bigdata
hdfs dfs -put datos_colombia.csv /user/hadoop/tarea_bigdata/
spark-submit batch_processor.py
```

## 🔄 Procesamiento Streaming

Abrir 5 terminales para iniciar los servicios y procesos:

| Terminal | Acción | Comando |
|-----------|--------|---------|
| 1 | Iniciar Hadoop | start-all.sh |
| 2 | Iniciar ZooKeeper | cd ~/kafka_2.13-3.7.0 && bin/zookeeper-server-start.sh config/zookeeper.properties |
| 3 | Iniciar Kafka Broker | cd ~/kafka_2.13-3.7.0 && bin/kafka-server-start.sh config/server.properties |
| 4 | Productor Kafka | python3 producer.py |
| 5 | Spark Streaming | spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 stream_processor.py |

## 📚 Créditos

**Autor:** Keidys Vanegas  
**Fecha:** Octubre 2025
