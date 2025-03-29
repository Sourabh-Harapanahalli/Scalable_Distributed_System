# Task 2: Optimizing Repartitioning and Parallelism

## Introduction
Task 2 focuses on optimizing the PageRank implementation by adjusting repartitioning and parallelism settings in Apache Spark. Properly distributing data across the cluster enhances performance and reduces execution time.

## Optimization Strategies
### 1. **Repartitioning the DataFrame**
   - The dataset is large, and default partitions may cause uneven distribution of data.
   - To ensure even workload distribution, we increase the number of partitions:
     ```python
     df = df.repartition(100)
     ```
   - This allows Spark to parallelize tasks efficiently, improving performance.

### 2. **Optimizing Shuffle and Parallelism Settings**
   - We configure Spark execution parameters to enhance data processing and balancing:
     ```shell
     --conf spark.sql.shuffle.partitions=100
     --conf spark.default.parallelism=100
     ```
   - This ensures that shuffle operations occur in a distributed manner, reducing execution bottlenecks.

### 3. **Execution Configuration for Better Performance**
   - Adjusted memory and core settings in the `spark-submit` command to better utilize cluster resources:
     ```shell
     --executor-memory 25G \
     --executor-cores 4 \
     --num-executors 8
     ```
   - This helps in balancing memory consumption and CPU utilization across nodes.

## Expected Outcome
- Improved load balancing across Spark workers.
- Faster job execution due to efficient partitioning.
- Reduced data skew and better memory management.

## Conclusion
Task 2 introduces data partitioning and parallelism optimizations that significantly improve Spark job execution, ensuring better scalability and efficiency in the PageRank algorithm.