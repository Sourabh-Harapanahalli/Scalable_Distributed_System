
### `part2_sorting/run.sh`
```bash
#!/bin/bash

echo "Create IoT dataset directory to HDFS..."
docker exec nn hdfs dfs -mkdir -p hdfs://nn:9000/iotDataset

echo "Copy IoT dataset directory to Nodes..."
docker cp /proj/umich-d-cs-edu-PG0/iotDataset/export.csv nn:/tmp/export.csv


echo "Uploading IoT dataset to HDFS..."
docker exec nn hdfs dfs -put /tmp/export.csv hdfs://nn:9000/iotDataset/export.csv

echo "Submitting IoT sorting job to Spark..."
docker exec master spark-submit --master spark://master:7077 /src/sort_iot.py

echo "Sorting job complete!"
