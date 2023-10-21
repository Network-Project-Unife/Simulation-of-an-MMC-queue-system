from MMC_system import MMC_system


def print_results(queue_system):
    print(f"Probabilita' di avere stato 0 = {queue_system.state_0_probability}")
    print(f"Probabilita' di avere stato k = {queue_system.state_k_probability}")
    print(f"Numero medio di pacchetti in coda: {queue_system.average_queue_length}")
    print(f"Numero medio di pacchetti nel sistema: {queue_system.average_system_length}")
    print(f"Tempo medio di attesa in coda: {queue_system.average_queue_waiting_time}")
    print(f"Tempo medio di attesa nel sistema: {queue_system.average_system_waiting_time}")


def main():
    servers = int(input("Inserire il numero dei servitori: "))
    arrival_rate = float(input("Inserire il tasso di nascita: "))
    service_rate = float(input("Inserire il tasso di morte: "))
    queue_system = MMC_system(servers, arrival_rate, service_rate)
    print_results(queue_system)
    

if __name__ == "__main__":
    main()