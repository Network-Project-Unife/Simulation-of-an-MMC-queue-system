import simpy
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Parametri della simulazione
ARRIVAL_RATE = 5  # Tasso di arrivo (lambda)
SERVICE_RATE = 6  # Tasso di servizio (mu)
NUM_SERVERS = 2   # Numero di server (c)
SIMULATION_TIME = 1000  # Tempo totale di simulazione
NUM_SIMULATIONS = 100  # Numero di simulazioni da eseguire

# Liste per salvare le statistiche
queue_lengths = []
system_lengths = []
waiting_times = []

for _ in range(NUM_SIMULATIONS):
    # Funzione per la generazione casuale di tempi di arrivo ed elaborazione
    def random_exp(lmbda):
        return -1 / lmbda * math.log(random.random())

    # Funzione per il processo di arrivo
    def customer_arrival(env, server, arrival_rate, service_rate):
        while True:
            yield env.timeout(random_exp(arrival_rate))
            env.process(customer_service(env, server, service_rate))

    # Funzione per il processo di servizio
    def customer_service(env, server, service_rate):
        with server.request() as request:
            yield request
            yield env.timeout(random_exp(service_rate))

    # Inizializzazione dell'ambiente di simulazione
    env = simpy.Environment()

    # Creazione del server
    server = simpy.Resource(env, capacity=NUM_SERVERS)

    # Avvio del processo di arrivo dei clienti
    for _ in range(NUM_SERVERS):
        env.process(customer_arrival(env, server, ARRIVAL_RATE, SERVICE_RATE))

    # Esecuzione della simulazione
    env.run(until=SIMULATION_TIME)

    # Calcolo delle metriche
    queue_lengths.append(server.queue_length)
    system_lengths.append(server.count)
    waiting_times.append(sum(server.queue_length for server in server.servers) / server.count)

# Calcolo delle statistiche medie
avg_queue_length = np.mean(queue_lengths)
avg_system_length = np.mean(system_lengths)
avg_waiting_time = np.mean(waiting_times)

# Calcolo delle metriche teoriche
rho = ARRIVAL_RATE / (NUM_SERVERS * SERVICE_RATE)
P0 = 1 / sum([(rho ** k) / math.factorial(k) for k in range(NUM_SERVERS)])  # Probabilità dello stato 0
Lq = ((rho ** (NUM_SERVERS + 1)) * P0) / ((math.factorial(NUM_SERVERS - 1)) * ((1 - rho) ** 2))  # Lunghezza della coda
Ws = Lq / ARRIVAL_RATE  # Tempo medio di attesa nel sistema
Wq = Ws - (1 / SERVICE_RATE)  # Tempo medio di attesa nella coda

# Stampa delle statistiche
print(f"Media lunghezza della coda (Simulazione): {avg_queue_length:.2f}")
print(f"Media lunghezza del sistema (Simulazione): {avg_system_length:.2f}")
print(f"Media tempo di attesa (Simulazione): {avg_waiting_time:.2f}")

print(f"Media lunghezza della coda (Teorica): {Lq:.2f}")
print(f"Media tempo di attesa nel sistema (Teorica): {Ws:.2f}")
print(f"Media tempo di attesa nella coda (Teorica): {Wq:.2f}")

# Grafico delle curve teoriche vs. simulazione in funzione di lambda
arrival_rates = np.linspace(1, 10, 10)
simulated_queue_lengths = []
simulated_waiting_times = []

for lmbda in arrival_rates:
    # Simulazione
    queue_lengths = []
    waiting_times = []
    for _ in range(NUM_SIMULATIONS):
        env = simpy.Environment()
        server = simpy.Resource(env, capacity=NUM_SERVERS)
        for _ in range(NUM_SERVERS):
            env.process(customer_arrival(env, server, lmbda, SERVICE_RATE))
        env.run(until=SIMULATION_TIME)
        queue_lengths.append(np.mean(server.queue_length))
        waiting_times.append(np.mean([w for w in waiting_times]))

    simulated_queue_lengths.append(np.mean(queue_lengths))
    simulated_waiting_times.append(np.mean(waiting_times))

# Plot delle curve teoriche vs. simulazione
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(arrival_rates, simulated_queue_lengths, marker='o', label='Simulazione')
plt.plot(arrival_rates, [rho ** (NUM_SERVERS + 1) / (math.factorial(NUM_SERVERS - 1) * (1 - rho) ** 2) for rho in arrival_rates], label='Teorica')
plt.xlabel('Tasso di Arrivo (lambda)')
plt.ylabel('Lunghezza della Coda (Lq)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(arrival_rates, simulated_waiting_times, marker='o', label='Simulazione')
plt.plot(arrival_rates, [(rho ** (NUM_SERVERS + 1)) / ((math.factorial(NUM_SERVERS - 1)) * ((1 - rho) ** 2) * lmbda) for rho, lmbda in zip(arrival_rates, SERVICE_RATE)], label='Teorica')
plt.xlabel('Tasso di Arrivo (lambda)')
plt.ylabel('Tempo di Attesa nella Coda (Wq)')
plt.legend()

plt.show()