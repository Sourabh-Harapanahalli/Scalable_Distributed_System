
---

### **`part1_setup/run.sh`**
```bash
#!/bin/bash

echo "===== Initializing Docker Swarm ====="
docker swarm init --advertise-addr 10.10.1.1

echo "===== Creating Overlay Network ====="
docker network create -d overlay --attachable spark_net

echo "===== Deploying Hadoop Distributed File System (HDFS) ====="
echo "Launching NameNode on node0..."
docker run -d --name nn --network spark_net -p 9870:9870 -v /data:/data hdfs-namenode

echo "Launching DataNodes across all nodes..."
docker service create --name dn --network spark_net --replicas 3 --mount type=bind,source=/data,target=/data hdfs-datanode

echo "===== Deploying Apache Spark ====="
echo "Launching Spark Master on node0..."
docker run -d --name master --network spark_net -p 8080:8080 -p 4040:4040 -p 18080:18080 -v /data:/data spark-master

echo "Launching Spark Workers across all nodes..."
docker service create --name worker --network spark_net --replicas 3 --mount type=bind,source=/data,target=/data spark-worker

echo "===== Cluster Setup Complete! ====="
echo "Check Spark UI at http://10.10.1.1:8080 and HDFS UI at http://10.10.1.1:9870"
