import os
import time
import random

class Producer:
    def __init__(self, text_folder, queue, queue_lock, empty_sem, full_sem, num_consumers):  # Добавляем num_consumers в конструктор
        self.text_folder = text_folder
        self.queue = queue
        self.queue_lock = queue_lock  # Мьютекс для синхронизации доступа к очереди
        self.empty_sem = empty_sem    # Семафор для отслеживания свободных мест в очереди
        self.full_sem = full_sem      # Семафор для отслеживания заполненных мест в очереди
        self.num_consumers = num_consumers  # Сохраняем num_consumers

    def read_texts(self):
        for filename in os.listdir(self.text_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.text_folder, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.empty_sem.acquire()  # Ждем, пока не появится свободное место в очереди
                    self.queue_lock.acquire()  # Блокируем доступ к очереди
                    self.queue.put((filename, text))  # Добавляем элемент в очередь
                    free_places = self.empty_sem._value
                    #print(f"Free places in queue: {free_places}. (Producer's action)", flush=True)
                    self.queue_lock.release()  # Разблокируем доступ к очереди
                    self.full_sem.release()    # Увеличиваем счетчик заполненных мест
                    sleep_time = random.uniform(1,2)
                    time.sleep(sleep_time)
                    print(f"Producer add file '{filename}' to queue. Time spent: {sleep_time:.2f}", flush=True)
        # Сигнал завершения для Consumer
        for _ in range(self.num_consumers):  # Используем self.num_consumers
            self.empty_sem.acquire()
            self.queue_lock.acquire()
            self.queue.put((None, None))  # Сигнал завершения
            self.queue_lock.release()
            self.full_sem.release()