import statistics
from MMcQueue import MMcQueue


def print_calculated_parameters(queue):
    average_service_length = statistics.mean(queue.system_lengths)
    average_queue_length = statistics.mean(queue.queue_lengths)
    average_system_length = average_service_length + average_queue_length
    average_queue_waiting_time = statistics.mean(queue.queue_waiting_times)
    average_system_waiting_time = statistics.mean(queue.system_waiting_times)
    print("\n===============Parametri della simulazione===============")
    print(f"Numero medio di pacchetti in servizio: {average_service_length}")
    print(f"Numero medio di pacchetti in coda: {average_queue_length}")
    print(f"Numero medio di pacchetti nel sistema: {average_system_length}")
    print(f"Tempo medio di attesa in coda: {average_queue_waiting_time}")
    print(f"Numero medio di attesa nel sistema: {average_system_waiting_time}")


def print_parameters(queue):
    print("\n=======Elementi caratteristici del sistema a coda=======")
    print(f"Probabilitá di avere stato 0 = {queue.state_0_probability * 100}%")
    print(f"Probabilitá di avere tutti i servitori occupati = {queue.queue_probability * 100}%")
    print(f"Numero medio di pacchetti in servizio: {queue.average_service_length}")
    print(f"Numero medio di pacchetti in coda: {queue.average_queue_length}")
    print(f"Numero medio di pacchetti nel sistema: {queue.average_system_length}")
    print(f"Tempo medio di attesa in coda: {queue.average_queue_waiting_time}")
    print(f"Tempo medio di attesa nel sistema: {queue.average_system_waiting_time}")


def main():
    num_servers = int(input("Inserire il numero dei servitori: "))
    arrival_rate = float(input("Inserire il tasso di nascita: "))
    service_rate = float(input("Inserire il tasso di morte: "))
    num_customers = int(input("Inserire il numero di clienti da simulare: "))
    queue = MMcQueue(num_servers, arrival_rate, service_rate, num_customers)
    queue.run()
    print_parameters(queue)
    print_calculated_parameters(queue)
    

if __name__ == "__main__":
    main()