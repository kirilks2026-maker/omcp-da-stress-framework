import time
from web3 import Web3

# --- НАСТРОЙКИ СЕТИ И ГЛАВНОГО КОШЕЛЬКА ---
RPC_URL = "https://evmrpc-testnet.0g.ai"
MAIN_PRIVATE_KEY = "YOUR_MAIN_PRIVATE_KEY"  # Вставь сюда свой приватный ключ с 30 OG

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("❌ Не удалось подключиться к RPC 0G!")
    exit(1)

main_account = w3.eth.account.from_key(MAIN_PRIVATE_KEY)
print(f"[➔] Главный кошелек: {main_account.address}")

balance_wei = w3.eth.get_balance(main_account.address)
balance_og = w3.from_wei(balance_wei, 'ether')
print(f"[➔] Баланс главного кошелька: {balance_og:.4f} OG")

if balance_og < 10.5:
    print("❌ Недостаточно средств для раздачи! Нужно минимум 10.5 OG.")
    exit(1)

generated_keys = []
amount_to_send = w3.to_wei(1.0, 'ether')  # Раздаем по 1 OG
chain_id = w3.eth.chain_id

print("\n=============================================================")
print("🚀 ГЕНЕРАЦИЯ 10 КОШЕЛЬКОВ И АВТОМАТИЧЕСКАЯ РАЗДАЧА ПО 1 OG")
print("=============================================================\n")

# Получаем текущий nonce главного кошелька
nonce = w3.eth.get_transaction_count(main_account.address)

for i in range(1, 11):
    # 1. Генерируем новый кошелек
    new_acc = w3.eth.account.create()
    generated_keys.append(new_acc.key.hex())
    print(f"[{i}/10] Новый адрес Sat_{i}: {new_acc.address}")

    # 2. Формируем транзакцию перевода 1 OG
    tx = {
        'nonce': nonce,
        'to': new_acc.address,
        'value': amount_to_send,
        'gas': 21000,
        'maxFeePerGas': w3.to_wei(2, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(1, 'gwei'),
        'chainId': chain_id
    }

    # 3. Подписываем и отправляем
    signed_tx = w3.eth.account.sign_transaction(tx, MAIN_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"     └─ Отправлен 1 OG | Tx Hash: {tx_hash.hex()}")

    nonce += 1
    time.sleep(1.0)  # Небольшая пауза между транзакциями

print("\n=============================================================")
print("✅ РАЗДАЧА ЗАВЕРШЕНА! СКОПИРУЙ ЭТОТ МАССИВ В BDA-СКРИПТ:")
print("=============================================================\n")

print("SELF_OPERATOR_KEYS = [")
for k in generated_keys:
    print(f'    "{k}",')
print("]")
