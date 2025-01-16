import time
import random

class Consumer:
    def __init__(self, queue, queue_lock, empty_sem, full_sem, consumer_id):
        self.queue = queue
        self.queue_lock = queue_lock  # Мьютекс для синхронизации доступа к очереди
        self.empty_sem = empty_sem    # Семафор для отслеживания свободных мест в очереди
        self.full_sem = full_sem      # Семафор для отслеживания заполненных мест в очереди
        self.consumer_id = consumer_id  # Идентификатор Consumer

    def process_texts(self):
        while True:
            self.full_sem.acquire()    # Ждем, пока в очереди не появится элемент
            self.queue_lock.acquire()  # Блокируем доступ к очереди
            filename, text = self.queue.get()  # Извлекаем элемент из очереди
            free_places = self.empty_sem._value
            #print(f"Free places in queue: {free_places}. (Consumer's action)", flush=True)
            self.queue_lock.release()  # Разблокируем доступ к очереди
            self.empty_sem.release()   # Увеличиваем счетчик свободных мест


            if filename is None:  # Проверяем сигнал завершения
                break

            # Обработка текста
            word_count = len(text.split())
            sleep_time = random.uniform(5, 6)
            time.sleep(sleep_time)
            print(f"Consumer {self.consumer_id} processed file '{filename}' with {word_count} words. Time spent: {sleep_time:.2f}", flush=True)