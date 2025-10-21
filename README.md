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
## Inicio de Servicios de Hadoop (HDFS y YARN)
Antes de ejecutar cualquier comando de Spark/HDFS, verifica que los servicios estén activos
Inicia con el usuario donde tengas hadoop instalado. 
# 1. Iniciar el sistema de archivos distribuido (HDFS)
start-dfs.sh
# 2. Iniciar el gestor de recursos (YARN)
start-yarn.sh
# 3. Verificar que los procesos estén corriendo (debes ver NameNode, DataNode, ResourceManager, NodeManager)

## Descarga y Carga del Dataset a HDFS
Descarga el archivo CSV y cárgalo al directorio de HDFS que usará el script.
Descargar el archivo (ejecutar en tu máquina local o VM):
wget -O datos_colombia.csv https://www.datos.gov.co/api/views/xfif-myr2/rows.csv?accessType=DOWNLOAD

## crear un script PySpark (batch_processor.py) para realizar las tareas de Batch:
nano batch_processor.py
Código Python (batch_processor.py)


## Procesamiento Streaming

## Crea un nuevo archivo llamado producer.py 
nano producer.py 
Código del Productor de Kafka (producer.py)

## Crea un nuevo archivo llamado stream_processor.py
nano stream_processor.py
Código del Consumidor Spark Streaming (stream_processor.py)

## Abrir 5 terminales para iniciar los servicios y procesos:

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
