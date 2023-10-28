import tkinter as tk
from tkinter import messagebox
import plotly.graph_objects as go
import plotly.offline as pyo
import simpy
import statistics
from MMcQueue import MMcQueue


def get_input():
    root = tk.Tk()
    root.withdraw()  # Hides the main tkinter window

    root.title("Input Parameters")
    root.geometry("300x200")

    # cell for num_servers input
    label_servers = tk.Label(root, text="Inserire il numero dei servitori:")
    label_servers.pack()
    entry_servers = tk.Entry(root)
    entry_servers.pack()

    # cell for arrival_rate input
    label_arrival_rate = tk.Label(root, text="Inserire il tasso di nascita:")
    label_arrival_rate.pack()
    entry_arrival_rate = tk.Entry(root)
    entry_arrival_rate.pack()

    # cell for service_rate input
    label_service_rate = tk.Label(root, text="Inserire il tasso di morte:")
    label_service_rate.pack()
    entry_service_rate = tk.Entry(root)
    entry_service_rate.pack()

    # cell for num_customers input
    label_num_customers = tk.Label(root, text="Inserire il numero di clienti da simulare:")
    label_num_customers.pack()
    entry_num_customers = tk.Entry(root)
    entry_num_customers.pack()

    # input controls 
    def validate_input():
        num_servers = entry_servers.get()
        arrival_rate = entry_arrival_rate.get()
        service_rate = entry_service_rate.get()
        num_customers = entry_num_customers.get()

        if not (num_servers and arrival_rate and service_rate and num_customers):
            messagebox.showerror("Errore", "Inserisci tutti i valori.")
        elif (num_servers*service_rate > arrival_rate):
            messagebox.showerror("Errore", "Il prodotto tra servitori e uscite deve essere maggiore degli arrivi")
        else:
            root.destroy()  # Close the dialog window

    
    # confirmation button for validating the values in input and starting the program
    submit_button = tk.Button(root, text="Conferma", command=validate_input)
    submit_button.pack()

    root.mainloop()

    num_servers = float(entry_servers.get())
    arrival_rate = float(entry_arrival_rate.get())
    service_rate = float(entry_service_rate.get())
    num_customers = int(entry_num_customers.get())

    return num_servers, arrival_rate, service_rate, num_customers


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
    num_servers, arrival_rate, service_rate, num_customers = get_input()
    queue = MMcQueue(num_servers, arrival_rate, service_rate, num_customers)
    queue.run()
    print_parameters(queue)
    print_calculated_parameters(queue)
    def_graph(queue)
    

if __name__ == "__main__":
    main()