import queue
import threading
from producer import Producer
from consumer import Consumer

def main():
    text_folder = 'texts'
    q = queue.Queue(maxsize=4)  # Ограничиваем размер очереди
    queue_lock = threading.Lock()  # Мьютекс для синхронизации доступа к очереди
    empty_sem = threading.Semaphore(q.maxsize)  # Семафор для свободных мест
    full_sem = threading.Semaphore(0)  # Семафор для заполненных мест

    # Количество Consumer
    num_consumers = 3

    # Создаем Producer и передаем num_consumers
    producer = Producer(text_folder, q, queue_lock, empty_sem, full_sem, num_consumers)
    producer_thread = threading.Thread(target=producer.read_texts)

    # Создаем Consumer
    consumers = [Consumer(q, queue_lock, empty_sem, full_sem, i + 1) for i in range(num_consumers)]
    consumer_threads = [threading.Thread(target=consumer.process_texts) for consumer in consumers]

    # Запускаем Producer и Consumer
    producer_thread.start()
    for thread in consumer_threads:
        thread.start()

    # Ожидаем завершения Producer
    producer_thread.join()

    # Ожидаем завершения всех Consumer
    for thread in consumer_threads:
        thread.join()

    print("All texts processed.")

if __name__ == "__main__":
    main()