from MMC_system import MMC_system


def print_results(queue_system):
    print(f"Probabilita' di avere stato 0 = {queue_system.state_0_probability}")
    print(f"Probabilita' di avere stato k = {queue_system.state_k_probability}")
    print(f"Numero medio di pacchetti in coda: {queue_system.queue_expectancy}")
    print(f"Numero medio di pacchetti nel sistema: {queue_system.system_expectancy}")
    print(f"Tempo medio di attesa in coda: {queue_system.waiting_time_queue_expectancy}")
    print(f"Tempo medio di attesa nel sistema: {queue_system.waiting_time_system_expectancy}")


def main():
    servers = int(input("Inserire il numero dei servitori: "))
    arrival_rate = float(input("Inserire il tasso di nascita: "))
    service_rate = float(input("Inserire il tasso di morte: "))
    queue_system = MMC_system(servers, arrival_rate, service_rate)
    print_results(queue_system)
    

if __name__ == "__main__":
    main()