# Task 4: Final PageRank Optimization and Execution

## Introduction
Task 4 involves running the final optimized version of the PageRank algorithm using **Apache Spark**. The focus is on efficient execution, resource management, and performance tuning.

## Execution Setup
### 1. **Spark-Submit Command**
The following command is used to execute the PageRank script efficiently on the cluster:
```shell
docker exec master spark-submit \
  --master spark://master:7077 \
  --deploy-mode client \
  --driver-memory 25G \
  --executor-memory 25G \
  --executor-cores 4 \
  --num-executors 8 \
  --conf spark.sql.shuffle.partitions=100 \
  --conf spark.default.parallelism=100 \
  --conf spark.executor.cores=4 \
  --conf spark.task.cpus=1 \
  --conf spark.local.dir=/data/tmp_1 \
  --conf spark.storage.memoryFraction=0.4 \
  --conf spark.memory.fraction=0.5 \
  --conf spark.executor.memoryOverhead=4G \
  --conf spark.driver.memoryOverhead=4G \
  /src/pagerank.py \
  hdfs://nn:9000/wikidata/enwiki-pages-articles.csv \
  hdfs://nn:9000/output/pagerank_optimized
```

### 2. **Key Optimizations**
- **Increased Shuffle Partitions** (`spark.sql.shuffle.partitions=100`) to balance load.
- **Optimized Memory Usage** (`spark.memory.fraction=0.5`) to avoid excessive disk spilling.
- **Reduced Executor Memory Overhead** (`spark.executor.memoryOverhead=4G`) to prevent crashes.
- **Changed Local Directory for Temporary Storage** (`spark.local.dir=/data/tmp_1`) to avoid disk space issues.

### 3. **Handling Disk Space Issues**
- **Temporary storage moved to `/data/tmp_1`** instead of `/proj/umich-d-cs-edu-PG0/tmp`.
- **Limited executor memory usage** to avoid running out of space.

## Expected Outcome
- **Efficient execution** of the PageRank algorithm.
- **Balanced resource allocation**, reducing disk overuse.
- **Faster job completion** by reducing unnecessary data recomputation.

## Conclusion
Task 4 ensures the PageRank job runs optimally on a distributed Spark cluster by fine-tuning **execution settings**, **memory usage**, and **storage location**. This leads to a scalable and efficient processing pipeline.

