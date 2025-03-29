# Task 3: Persisting DataFrames for Optimization

## Introduction
Task 3 aims to optimize the PageRank computation by **persisting** key DataFrames in memory. This reduces redundant computations and improves Spark's efficiency by caching frequently used data.

## Optimization Strategies
### 1. **Persisting Input Data**
   - Instead of reloading the dataset in each iteration, the input DataFrame is **persisted** in memory:
     ```python
     df = df.repartition(100).persist()
     ```
   - This prevents unnecessary I/O operations and accelerates job execution.

### 2. **Persisting Ranks to Optimize Iterations**
   - The `ranks` DataFrame is frequently accessed, making it a good candidate for persistence:
     ```python
     ranks = df.select("page_title").distinct().withColumn("rank", lit(1.0)).persist()
     ```
   - Persisting `ranks` ensures that its computed values are reused efficiently across iterations.

### 3. **Unpersisting Old Data to Free Memory**
   - To avoid excessive memory usage, the previous iteration's `ranks` DataFrame is **unpersisted** before updating:
     ```python
     ranks.unpersist()
     ranks = contribs.withColumnRenamed("neighbor", "page_title") \
                     .withColumn("rank", 0.15 + 0.85 * col("total_contrib")).persist()
     ```
   - This ensures that outdated data is removed and does not consume unnecessary resources.

## Expected Outcome
- **Reduced computation time** due to cached DataFrames.
- **Less redundant recomputation**, improving Spark job efficiency.
- **Optimized memory usage** by freeing up unneeded data.

## Conclusion
Persisting key DataFrames significantly **improves Spark's performance** by reducing expensive recomputation. Task 3 ensures that iterations are efficiently executed with minimal resource wastage.