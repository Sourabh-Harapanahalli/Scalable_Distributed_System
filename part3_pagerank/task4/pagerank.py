from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sum as spark_sum

# Initialize Spark session
spark = SparkSession.builder.appName("PageRank").getOrCreate()

# Read input data from HDFS
df = spark.read.csv("hdfs://nn:9000/pagerank/enwiki-latest-pages-articles.csv", header=True, sep=",") \
       .select("page_title", "neighbor")

# Repartition data to optimize shuffle performance
df = df.repartition(100).persist()

# Initialize ranks with equal probability
ranks = df.select("page_title").distinct().withColumn("rank", lit(1.0)).persist()

# Run PageRank for 10 iterations
for _ in range(10):
    contribs = df.join(ranks, "page_title") \
                 .groupBy("neighbor") \
                 .agg(spark_sum(col("rank") / 2).alias("total_contrib"))
    
    # Unpersist old ranks to free memory
    ranks.unpersist()
    
    # Update ranks with damping factor
    ranks = contribs.withColumnRenamed("neighbor", "page_title") \
                    .withColumn("rank", lit(0.15) + lit(0.85) * col("total_contrib")) \
                    .persist()

# Save the final computed ranks to HDFS
ranks.write.csv("hdfs://nn:9000/pagerank/output", mode="overwrite")

# Stop Spark session
spark.stop()