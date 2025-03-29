# Part 2: Sorting IoT Data

This script loads IoT data from HDFS, sorts it by country code and timestamp, and writes the output back to HDFS.

## Execution
Run:
```bash
bash run.sh

The sortData.py script sorts input data based on the columns 'cca2' and 'timestamp' using Apache Spark. The output file is written to hdfs in a .csv format.

1. Navigate to the dataset directory:
cd /proj/umich-d-cs-edu-PG0/iotDataset/

2. Copy the dataset (export.csv) to HDFS using the `docker cp` command

3. Start an interactive shell session in the Spark master container:
docker exec -it <containerid> /bin/bash

4. Open the file editor (nano) inside the container and create the Python script:
nano sorting_iot.py
- Copy and paste the **sorting_iot.py** code.
- Save the file (`CTRL+X`, then `Y`, and press `ENTER`).

5. Submit the Spark job using `spark-submit` inside the container
Spark-submit sort_iot.py.

6. To view the result of the sorted data use hdfs dfs command
hdfs dfs -tail /sorted_output.csv


This process ensures that the dataset is loaded into HDFS, processed using Spark, and sorted results are saved and viewed 
