import os
import subprocess
import threading
import time
import random

class OGStorageDAShooter:
    def __init__(self):
        """
        Phase 2: Direct 0G Storage DA Ingestion Framework.
        Bypasses standard contract interactions to test raw sharding bandwidth.
        """
        # Официальные параметры тестнета Galileo
        self.blockchain_rpc = "https://evmrpc-testnet.0g.ai"
        self.indexer_url = "https://indexer-storage-testnet-turbo.0g.ai"
        
        # --- ТВОЙ СКРЫТЫЙ ПРИВАТНЫЙ КЛЮЧ ---
        self.operator_key = "ТВОЙ_ПРИВАТНИК_СЮДА" 
        
        # Конфигурация нагрузки: 200 тяжелых файлов по 350 МБ (Всего 70 ГБ)
        self.chunk_size_mb = 350
        self.total_chunks = 200
        
        # Ограничиваем параллельность (например, до 3 одновременных тяжелых потоков),
        # чтобы GitHub Codespaces или сама нода не падали по таймауту сети.
        self.semaphore = threading.Semaphore(3)

    def setup_binary_env(self):
        """Автоматически разворачивает окружение 0g-storage-client прямо в облаке"""
        if not os.path.exists("./0g-storage-client"):
            print("[➔] Downloading official 0G Storage CLI client into cloud pipes...")
            # Скачиваем официальный скомпилированный клиент для Linux (Codespaces крутится на Ubuntu)
            # Примечание: URL релиза может обновляться в репозитории 0gfoundation
            try:
                # Если бинарника нет, качаем его исходники/релиз или собираем. 
                # Предполагаем, что ты закинул скомпилированный бинарник '0g-storage-client' в корень проекта.
                print("[!] Ensure '0g-storage-client' binary is present in this directory and has execution rights.")
                subprocess.run("chmod +x 0g-storage-client", shell=True)
            except Exception as e:
                print(f"[❌ ENV ERROR] Failed to set permissions: {str(e)}")

    def push_heavy_sector(self, chunk_id):
        with self.semaphore:
            file_name = f"sat_telemetry_chunk_{chunk_id:03d}.raw"
            try:
                print(f"\n[STREAM #{chunk_id:03d}] 🛰️ Allocating {self.chunk_size_mb}MB in cloud virtual RAM...")
                
                # Генерируем тяжелый сектор данных прямо на лету в Codespaces
                with open(file_name, "wb") as f:
                    f.write(os.urandom(self.chunk_size_mb * 1024 * 1024))
                
                print(f"[STREAM #{chunk_id:03d}] 🚀 Launching high-speed DA ingestion pipeline...")
                start_time = time.time()
                
                # Собираем нативную CLI команду по официальной спецификации 0G Labs
                cmd = (
                    f"./0g-storage-client upload "
                    f"--url {self.blockchain_rpc} "
                    f"--key {self.operator_key} "
                    f"--indexer {self.indexer_url} "
                    f"--file {file_name}"
                )
                
                # Запускаем отправку. Твой мобильный интернет не тратится, качает сеть Microsoft/GitHub!
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                
                duration = time.time() - start_time
                speed = self.chunk_size_mb / duration
                
                print(f"[✓ SUCCESS #{chunk_id:03d}] Ingested in {duration:.2f}s | Speed: {speed:.2f} MB/s")
                
            except subprocess.CalledProcessError as e:
                print(f"[❌ DROP #{chunk_id:03d}] CLI Ingestion rejected by Indexer -> {e.stderr}")
            except Exception as e:
                print(f"[❌ ERROR #{chunk_id:03d}] Internal failure -> {str(e)}")
            finally:
                # Жесткое правило: удаляем файл при любом раскладе, чтобы не переполнить хранилище Codespaces
                if os.path.exists(file_name):
                    os.remove(file_name)

    def execute_da_cascade(self):
        print("=============================================================")
        print("LAUNCHING PHASE 2: SERVER-TO-SERVER DIRECT DA STORAGE STORM")
        print(f"Target Configuration: {self.total_chunks} Chunks x {self.chunk_size_mb}MB (~70.0 GB)")
        print("Bypassing on-chain mempool. Stress-testing raw sharding limits.")
        print("=============================================================")
        
        self.setup_binary_env()
        
        threads = []
        for i in range(1, self.total_chunks + 1):
            t = threading.Thread(target=self.push_heavy_sector, args=(i,))
            threads.append(t)
            t.start()
            # Пауза в 1 секунду между запуском потоков, чтобы плавно разгонять сетевую трубу
            time.sleep(1.0) 

        for t in threads:
            t.join()
            
        print("\n=============================================================")
        print("🚀 STRESS TESTING PIPELINE CONCLUDED. MONITOR STORAGE SCAN NOW.")
        print("=============================================================")

if __name__ == "__main__":
    shooter = OGStorageDAShooter()
    # shooter.execute_da_cascade() # Запускай, когда скачаешь бинарник в папку
