# 🛰️ 0G Galileo Data Availability (DA) Stress Framework

An industrial-grade, multi-threaded stress-testing framework designed to benchmark raw sharding ingestion bandwidth and storage limits on the **0G Labs (Galileo Testnet)** Data Availability (DA) layer.

---

## 📌 Architecture Overview

Unlike standard smart-contract execution tools, this framework bypasses the EVM mempool entirely to directly target the **0G Storage DA Ingestor and Turbo Indexer**. It generates ephemeral, heavy data sectors in cloud virtual RAM (e.g., GitHub Codespaces) and pushes them over high-speed server-to-server pipes.

[Master Wallet] ──(dispenser.py)──> [10 Operator Accounts]
│
(da_stress_test.py)
│
[70 GB Data Ingestion]
│
▼
[0G Ingester / Turbo Indexer Node]

---

## 🚀 Key Modules

### 1. Account Dispenser (`dispenser.py`)
- **Purpose**: Automated sub-wallet generation and gas distribution[cite: 10].
- **Functionality**:
  - Automatically provisions 10 sub-operator accounts[cite: 10].
  - Signs and broadcasts batch funding transactions (`1.0 OG` each) using dynamic EIP-1559 gas pricing and safe nonce increments[cite: 10].
  - Formats output arrays directly for ingestion into execution scripts[cite: 10].

### 2. Direct DA Storage Ingestor (`da_stress_test.py`)
- **Purpose**: Direct sharding layer bandwidth & capacity benchmarking.
- **Functionality**:
  - Spawns multi-threaded execution loops controlled via `threading.Semaphore(3)` to prevent network rate-limiting/timeouts.
  - Dynamically creates 350 MB raw data sectors in memory and feeds them into the official `0g-storage-client` CLI binary.
  - Automatically handles garbage collection / ephemeral disk cleanup to operate continuously inside cloud containers.
  - Targets `https://indexer-storage-testnet-turbo.0g.ai`[cite: 9].

---

## 🛠️ Quick Start & Usage

### 1. Prerequisites & Environment
Ensure Python 3.10+ and `web3.py` are installed:
```bash
pip install web3 python-dotenv
```
Make sure the official 0g-storage-client binary is placed in the root directory with executable permissions:
```
chmod +x 0g-storage-client
```
2. Provision Operator Accounts
Configure your primary funding private key in dispenser.py and run:
```
python3 dispenser.py
```
Copy the generated SELF_OPERATOR_KEYS array into da_stress_test.py.
3. Launch the Storage Cascade
```
python3 da_stress_test.py
```

📊 Benchmarking Metrics Tracked
Ingestion Latency: Time-to-ingest per 350 MB chunk[cite: 9].

Throughput Speed: Real-time MB/s bandwidth per stream[cite: 9].

RPC / Indexer Rejections: Detection of connection ceiling limits (e.g., Error -32005) under load[cite: 9].

⚠️ Safety & Environment Notice
This tool is built for official testnet benchmarking and infrastructure stress testing only. Always ensure running inside isolated cloud runtime environments (e.g., GitHub Codespaces) to prevent local network saturation or disk overflow[cite: 9].
