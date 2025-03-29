from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sum as spark_sum, count, when

# ✅ Initialize Spark Session with Performance Optimizations
spark = SparkSession.builder \
    .appName("PageRank") \
    .config("spark.sql.shuffle.partitions", "50") \
    .getOrCreate()

# ✅ Read Input Data with Proper Partitioning
df = spark.read.csv("hdfs://nn:9000/wikidata/enwiki-pages-articles/enwiki-latest-pages-articles.csv",
                    header=True, sep=",") \
               .select("page_title", "neighbor")

df = df.repartition(20)  # Adjust partition count for better parallelism

# ✅ Count Outgoing Links per Page
outgoing_links = df.groupBy("page_title").agg(count("neighbor").alias("num_links"))

# Prevent division by zero
outgoing_links = outgoing_links.withColumn("num_links", when(col("num_links") == 0, lit(1)).otherwise(col("num_links")))

# ✅ Initialize Page Ranks
ranks = df.select("page_title").distinct().withColumn("rank", lit(1.0))

# ✅ Run PageRank for 10 Iterations
for _ in range(10):
    contribs = df.join(ranks, "page_title") \
                 .join(outgoing_links, "page_title") \
                 .withColumn("contrib", col("rank") / col("num_links")) \
                 .groupBy("neighbor") \
                 .agg(spark_sum(col("contrib")).alias("total_contrib"))

    ranks = contribs.withColumnRenamed("neighbor", "page_title") \
                    .withColumn("rank", lit(0.15) + 0.85 * col("total_contrib"))

# ✅ Save Output with Optimized Partitions
ranks.coalesce(1).write.csv("hdfs://nn:9000/pagerank/output", mode="overwrite", header=True)

# ✅ Stop Spark
spark.stop()