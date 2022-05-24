# CockroachDB

## CockroachDB overview

<p float="left">
    <img src="pix/kv_mappings.png" width="600" />
</p>

* CockroachDB prioritizes `consistency` over `availability`.
* CockroachDB prioritizes `transactional` workloads over `analytic` workloads.

<p float="left">
    <img src="pix/cap.png" width="400" />
</p>

* `Scalability`: The CockroachDB distributed architecture allows a cluster to scale seamlessly as workload increases or decreases.
* `High availability`: CockroachDB can continue operating if a node, zone, or region fails without compromising availability.
* `Consistency`: CockroachDB provides the highest practical level of transactional isolation and consistency.
* `Performance`: The CockroachDB architecture is designed to support low-latency and high-throughput transactional workloads.
* `Geo-partitioning`: CockroachDB allows data to be physically located in specific localities to enhance performance for localized applications and to respect data sovereignty requirements.
* `Compatibility`: CockroachDB implements ANSI-standard SQL and is wire-protocol compatible with PostgreSQL.
* `Portability`: The CockroachDB architecture is very well aligned with containerized deployment options, and in particular, with Kubernetes. 

## CockroachDB architecture

<p float="left">
    <img src="pix/layered_process.png" width="350" />
</p>

* The `SQL layer` accepts SQL requests in the PostgreSQL wire protocol. It parses and optimizes the SQL requests and translates the requests into KV operations that can be processed by lower layers.
* The `transaction layer` is responsible for ensuring ACID transactions and serializable isolation. It ensures that transactions see a consistent view of data and that modifications occur as if they had been executed one at a time.
* The `distribution layer` is responsible for the partitioning of data into ranges and the distribution of those ranges across the cluster. It is responsible for managing range leases and assigning leaseholders.
* The `replication layer` ensures that data is correctly replicated across the cluster to allow high availability in the event of a node failure.
* The `storage layer` is responsible for the persistence of data to local disk and the processing of low-level queries and updates on that data.

<p float="left">
    <img src="pix/lsm_writes.png" width="450" />
    <img src="pix/lsm_reads.png" width="450" />
</p>
