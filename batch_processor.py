from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnull, regexp_extract, trim, avg, lit
from pyspark.sql.types import IntegerType, DateType, DoubleType

HDFS_INPUT_PATH = "hdfs://BIGDATA3:9000/user/hadoop/tarea_bigdata/datos_colombia.csv"
HDFS_OUTPUT_PATH = "hdfs://BIGDATA3:9000/user/hadoop/tarea_bigdata/resultados_batch_limpio.parquet"
APP_NAME = "TareaBigData_ProcesamientoBatch"

def clean_data(df):
    df_count_original = df.count()
    df_cleaned = df.filter(
        (col("Etnia") != "ND") &
        (col("TipoAsignacionBeneficio") != "ND") &
        (col("TipoPoblacion") != "ND")
    )
    print(f"Registros eliminados por 'ND' en clave: {(df_count_original - df_cleaned.count())}")
    df_cleaned = df_cleaned.withColumn(
        "Pais",
        when(
            col("Pais").isNull() | (col("Pais") == "ND"),
            lit("COLOMBIA")
        ).otherwise(col("Pais"))
    )
    df_count_original_2 = df_cleaned.count()
    df_cleaned = df_cleaned.filter(col("FechaUltimoBeneficioAsignado") != "1900-01-01")
    print(f"Registros eliminados por fecha histórica: {(df_count_original_2 - df_cleaned.count())}")
    df_cleaned = df_cleaned.dropna(subset=["CodigoDepartamentoAtencion"])
    return df_cleaned

def transform_data(df):
    df = df.withColumn(
        "BeneficioConsolidado_MIN",
        regexp_extract(col("RangoBeneficioConsolidadoAsignado"), r"\$(\d+\.?\d*\.?\d+)\s", 1)
    ).withColumn(
        "BeneficioConsolidado_MIN",
        col("BeneficioConsolidado_MIN").cast(DoubleType())
    )
    df = df.withColumn(
        "Edad_MIN",
        regexp_extract(col("RangoEdad"), r"(\d+)-", 1).cast(IntegerType())
    )
    df = df.withColumn(
        "CantidadDeBeneficiarios",
        col("CantidadDeBeneficiarios").cast(IntegerType())
    )
    df_final = df.select(
        "Bancarizado",
        "CodigoDepartamentoAtencion",
        "NombreDepartamentoAtencion",
        "Etnia",
        "Genero",
        "Edad_MIN",
        "CantidadDeBeneficiarios",
        "BeneficioConsolidado_MIN",
        "EstadoBeneficiario",
        col("FechaInscripcionBeneficiario").cast(DateType()).alias("FechaInscripcion")
    )
    return df_final

def main():
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    print("\n--- INICIO PROCESAMIENTO BATCH: CARGA ---")
    df = spark.read.csv(HDFS_INPUT_PATH, header=True, inferSchema=True)
    df_limpio = clean_data(df)
    df_final = transform_data(df_limpio)
    df_final.select(avg(col("Edad_MIN")).alias("Edad_Promedio")).show()
    print("\n--- ALMACENAMIENTO ---")
    df_final.write.mode("overwrite").parquet(HDFS_OUTPUT_PATH)
    print(f"Resultados almacenados exitosamente en HDFS: {HDFS_OUTPUT_PATH}")
    spark.stop()

if __name__ == "__main__":
    main()
