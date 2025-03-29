import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    spark = SparkSession.builder \
        .appName("sortData") \
        .getOrCreate()

    # Use the correct HDFS path with 'nn' as the NameNode
    input_file_path = "hdfs://nn:9000/export.csv"
    output_file_path = "hdfs://nn:9000/sorted_output"

    # Read the CSV file from HDFS
    data = spark.read.option("header", "true").csv(input_file_path)

    # Sort by 'cca2' and 'timestamp' columns
    sorted_data = data.orderBy(col("cca2"), col("timestamp"))

    # Save the sorted output as a single CSV file in HDFS
    sorted_data.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_file_path)

    print(f"Sorted data saved at: {output_file_path}")

    spark.stop()

if __name__ == "__main__":
    main()
