from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sum as spark_sum

# Initialize a Spark session for running the PageRank algorithm
spark = SparkSession.builder.appName("PageRank").getOrCreate()

# Read input data from HDFS
df = spark.read.csv("hdfs://nn:9000/pagerank/enwiki-latest-pages-articles.csv", header=True, sep=",") \
       .select("page_title", "neighbor")  # Selecting only the relevant columns

# Repartition the DataFrame into 100 partitions for better parallelism
df = df.repartition(100)

# Initialize ranks: Every unique page starts with a rank of 1.0
ranks = df.select("page_title").distinct().withColumn("rank", lit(1.0))

# Run the PageRank algorithm for 10 iterations
for _ in range(10):
    # Compute contributions from each page to its linked neighbors
    contribs = df.join(ranks, "page_title") \  # Join with ranks DataFrame on "page_title"
                 .groupBy("neighbor") \  # Group contributions by neighbor pages
                 .agg(spark_sum(col("rank") / 2).alias("total_contrib"))  # Compute sum of contributions

    # Update ranks based on contributions, using the PageRank formula
    ranks = contribs.withColumnRenamed("neighbor", "page_title") \
                    .withColumn("rank", 0.15 + 0.85 * col("total_contrib"))  # Apply damping factor

# Save the final PageRank results to HDFS
ranks.write.csv("hdfs://nn:9000/pagerank/output", mode="overwrite")

# Stop the Spark session
spark.stop()
