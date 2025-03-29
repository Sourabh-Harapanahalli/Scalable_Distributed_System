
### `part3_pagerank/run.sh`
```bash
#!/bin/bash

echo "Creating Directory PageRank dataset to HDFS..."
docker exec nn hdfs dfs -mkdir -p hdfs://nn:9000/wikidata

echo "Copying PageRank dataset to Nodes..."
docker cp ~/cisece578-a1/enwiki-latest-pages-articles.csv nn:/tmp/
docker cp ~/cisece578-a1/export.csv nn:/tmp/

echo "Uploading PageRank dataset to HDFS..."
docker exec nn hdfs dfs -put /tmp/enwiki-latest-pages-articles.csv hdfs://nn:9000/pagerank/enwiki-pages-articles/
docker exec nn hdfs dfs -put /tmp/export.csv hdfs://nn:9000/pagerank/enwiki-pages-articles/

echo "===== Running PageRank Spark Job with Configured Resources ====="

docker exec master spark-submit \
    --master spark://master:7077 \
    --driver-memory 30G \
    --executor-memory 30G \
    --executor-cores 5 \
    --conf spark.task.cpus=1 \
		/src/pagerank.py \
  hdfs://nn:9000/pagerank/enwiki-latest-pages-articles.csv \
  hdfs://nn:9000/pagerank/output

echo "PageRank job complete!"


echo "PageRank job for task 2,3,4 "
docker exec master spark-submit \
    --master spark://master:7077 \
    --driver-memory 30G \
    --executor-memory 30G \
    --executor-cores 5 \
    --conf spark.task.cpus=1 \
	--conf spark.sql.shuffle.partitions=100 \  # Matches repartition in the script
	  --conf spark.default.parallelism=100 \
	  --conf spark.executor.cores=4 \
	  --conf spark.task.cpus=1 \
	  --conf spark.local.dir=/data/tmp_1 \  # Set temp storage directory
	  --conf spark.storage.memoryFraction=0.4 \  # Limits memory use for storage
	  --conf spark.memory.fraction=0.5 \  # Prevents excessive memory allocation
	  --conf spark.executor.memoryOverhead=4G \  # Prevents OOM errors
	  --conf spark.driver.memoryOverhead=4G \
		/src/pagerank.py \
  hdfs://nn:9000/pagerank/enwiki-latest-pages-articles.csv \
  hdfs://nn:9000/pagerank/output
