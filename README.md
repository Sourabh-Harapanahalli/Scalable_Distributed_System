# Scalable Distributed System

## Overview
The **Scalable Distributed System** project aims to deploy and optimize **big data analytics infrastructure** using **Apache Hadoop** and **Apache Spark** on a **Docker Swarm** cluster. The project focuses on setting up a scalable and efficient data processing environment on **CloudLab**, leveraging containerized deployment techniques to manage and orchestrate distributed computing tasks across multiple virtual machines.

This implementation showcases the **deployment, configuration, and execution of distributed applications** on a fault-tolerant and parallel computing system. It also includes developing and optimizing a **PageRank algorithm** using **PySpark**, demonstrating efficient parallel processing, data partitioning, and memory optimization techniques. Additionally, the project incorporates **fault-tolerance mechanisms** to ensure reliability in a distributed setting by simulating worker failures and analyzing Spark’s recovery mechanisms.

Through this project, we aim to:
- Gain hands-on experience with **Docker Swarm** for cluster management and networking.
- Deploy and configure **Hadoop Distributed File System (HDFS)** and **Apache Spark** for large-scale data processing.
- Implement **sorting algorithms** and **PageRank algorithm** using **PySpark**.
- Optimize Spark’s performance by tuning **data partitioning, shuffle operations, and memory management**.
- Evaluate system performance through **execution time analysis, task distribution, and resource utilization**.
- Explore Spark’s built-in **fault tolerance capabilities** and simulate worker failures to study recovery mechanisms.

This project is an excellent foundation for understanding **scalable distributed computing**, making it highly relevant for large-scale data processing applications in industry and research.


## Table of Contents
- [Environment Setup](#environment-setup)
- [Apache Hadoop & Spark Deployment](#apache-hadoop--spark-deployment)
- [Spark Applications](#spark-applications)
  - [Sorting Application](#sorting-application)
  - [PageRank Algorithm](#pagerank-algorithm)
- [Performance Analysis](#performance-analysis)
- [Lessons & Conclusions](#lessons--conclusions)

---

## Environment Setup
### **CloudLab Experiment Setup**
1. **Create CloudLab Experiment**
   - Use the `cisece578-win25-ch1-3node` profile under the `umich-d-cs-edu` project.
   - Start the experiment and note SSH commands for each VM.
2. **Experiment Constraints**
   - Each group can run **one** experiment under `umich-d-cs-edu`.
   - Experiments last **16 hours**; extend them as needed.
   - Retrieve SSH commands from CloudLab's experiment list.
3. **Generate SSH Keys & Set Up Access**
   ```sh
   ssh-keygen
   ```
   Retrieve the key:
   ```sh
   cat ~/.ssh/id_rsa.pub
   ```
   Append this key to `~/.ssh/authorized_keys` on **all VMs** for password-less SSH access.
4. **Additional Storage Setup**

### **Setting Up Docker Swarm**
1. **Install Docker & Build Images (on all nodes)**
2. **Initialize Swarm (on node 0 - Manager Node)**
   ```sh
   docker swarm init --advertise-addr <Node 0 Private IP>
   ```
3. **Join Worker Nodes**
   ```sh
   docker swarm join --token <TOKEN> <MANAGER_IP>:2377
   ```
4. **Create Overlay Network**
   ```sh
   docker network create --driver overlay spark_net
   ```

## Apache Hadoop & Spark Deployment
### **Deploying Apache Hadoop (HDFS) on Docker Swarm**
1. Launch **NameNode** (on node0)
2. Launch **DataNodes** (on node1 & node2)
3. **Verify Deployment**
   - Open `http://10.10.1.1:9870` to check the status of HDFS.

### **Deploying Apache Spark on Docker Swarm**
1. Launch **Spark Master** (on node0)
2. Launch **Spark Worker Nodes** (on node1 & node2)
3. **Verify Deployment**
   - Open `http://10.10.1.1:8080` to check the Spark UI.

## Spark Applications
### **Sorting Application**
1. **Load Data into HDFS**
   ```sh
   hdfs dfs -put /proj/umich-d-cs-edu-PG0/iotDataset/export.csv /path/in/hdfs
   ```
2. **Run Sorting Application**
   ```sh
   spark-submit --master spark://node0:7077 sort_iot.py
   ```
3. **Output Stored in HDFS**
   ```sh
   hdfs dfs -ls /sorted_output
   ```

### **PageRank Algorithm**
#### **Task 1: Basic Implementation**
- Implemented using **PySpark** and **HDFS** for storage.
- Iterates 10 times, distributing rank contributions to neighbors.

#### **Task 2: Optimized Version**
- **Partitioning Strategy:** `df.repartition(20)`
- **Shuffle Optimization:** `spark.sql.shuffle.partitions=50`
- **Handling Zero Outgoing Links:** Avoid division errors.
- **Optimized Output Storage:** `coalesce(1)` before writing.

#### **Task 3: Memory Optimization**
- **Persisting DataFrames** to reduce redundant computations.
- **Unpersisting Old Ranks** to free memory before reassigning.

#### **Task 4: Simulating Worker Failure**
- **Scaling Down Worker Services**:
  ```sh
  docker service scale spark_worker=2
  ```
- **Killing a Worker**:
  ```sh
  docker kill <worker_container_id>
  ```
- **Observing Spark UI** (`http://10.10.1.1:8080`) to check task reassignment.

## Performance Analysis
| Metric               | Task 1 (Baseline) | Task 2 (Optimized) |
|----------------------|------------------|--------------------|
| Execution Time      | ~379 sec (6.3 min) | ~616 sec (10.3 min) |
| Executors Used      | 15                 | 12                 |
| Shuffle Partitions  | 200 (default)      | 50 (optimized)     |
| Partitions Used     | 10                 | 20                 |

## Lessons & Conclusions
- **Parallelism:** Efficient use of multiple executors for distributing computations.
- **Performance Tuning:** Reducing shuffle overhead and optimizing memory management.
- **Fault Tolerance:** Spark's built-in recovery mechanisms ensure reliability.
- **Future Improvements:** Further tuning of partitioning and executor allocation.

---

### **How to Run the Project**
1. Clone the repository:
   ```sh
   git clone https://github.com/sourabh-harapanahalli/Scalable_Distributed_System.git
   cd Scalable_Distributed_System
   ```
2. Deploy on CloudLab (follow the setup instructions).
3. Run Spark applications using `spark-submit`.
4. Monitor execution using Spark UI.


