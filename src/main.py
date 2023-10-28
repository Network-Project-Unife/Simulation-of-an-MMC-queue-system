import plotly.graph_objects as go
import plotly.offline as pyo
import simpy
import statistics
from MMcQueue import MMcQueue


def def_graph(queue):
    # Extract the times and number of customers from the customers_history dictionary
    times = list(queue.customers_history.keys())
    num_customers = list(queue.customers_history.values())

    # Create line graph with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=num_customers, mode='lines', name='Numbers of customers'))
    fig.update_layout(title='Simulation of an M/M/C queue system',
                        xaxis_title='Time (0.1s)',
                        yaxis_title='Number of customers in the system')
    
    # set the interval between the x-axis ticks to 0.1 seconds
    fig.update_xaxes(tickmode='linear', tick0=0, dtick=0.1)

    # Create an html file contain the graph in the current directory
    pyo.plot(fig, filename='mmc_queue_graph.html')

    # Show the graph
    fig.show()


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
    def_graph(queue)
    

if __name__ == "__main__":
    main()