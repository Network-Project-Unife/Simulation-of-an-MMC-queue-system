import plotly.graph_objects as go
import re
import statistics
import tkinter as tk
from tkinter import messagebox

from MMcQueue import MMcQueue


def draw_graph(queue):
    # Extract the times and number of customers from the customers_history dictionary
    times = list(queue.customers_history.keys())
    customers_in_service = [i["service"] for i in list(queue.customers_history.values())]
    customers_in_queue = [i["queue"] for i in list(queue.customers_history.values())]
    customers_in_system = [i["system"] for i in list(queue.customers_history.values())]

    average_service_length = statistics.mean(customers_in_service)
    average_queue_length = statistics.mean(customers_in_queue)
    average_system_length = statistics.mean(customers_in_system)
    average_queue_waiting_time = statistics.mean(queue.queue_waiting_times)
    average_system_waiting_time = statistics.mean(queue.system_waiting_times)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=times,
        y=customers_in_service,
        name='Customers in service',
        #marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=times,
        y=customers_in_queue,
        name='Customers in queue',
        #marker_color='indianred'
    ))    
    fig.update_layout(
        title='Simulation of an M/M/C queue system',
        xaxis=dict(title='Time [s]', type='category',),
        yaxis=dict(title='Number of customers in the system'),
        legend=dict(title="Customers in the system"),
        barmode="stack"
    )

    # Show the graph
    fig.show()


def get_input():
    def validate_input():
        num_servers = entry_servers.get()
        arrival_rate = entry_arrival_rate.get()
        service_rate = entry_service_rate.get()
        num_customers = entry_num_customers.get()
        if "." in num_servers:
            messagebox.showerror("Errore", "Il numero dei server deve essere intero.")
            return
        if "." in num_customers:
            messagebox.showerror("Errore", "Il numero dei pacchetti deve essere intero.")
            return
        for inp in [num_servers, arrival_rate, service_rate, num_customers]:
            if not inp:
                messagebox.showerror("Errore", "Inserisci tutti i valori.")
                return
            if not re.match("[0-9]+(\.[0-9]+)?", inp):
                messagebox.showerror("Errore", "Valori numerici non validi.")
                return
        if (float(arrival_rate) / (int(num_servers) * float(service_rate))) >= 1:
            messagebox.showerror("Errore", "il fattore di utilizzo deve essere minore di 1 (numero di servitori * tasso di morte > tasso di nascita).")
            return
            
        inp_list[0] = int(num_servers)
        inp_list[1] = float(arrival_rate)
        inp_list[2] = float(service_rate)
        inp_list[3] = int(num_customers)
        root.destroy()  # Close the dialog window

    root = tk.Tk()

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

    # confirmation button for validating the values in input and starting the program
    submit_button = tk.Button(root, text="Conferma", command=validate_input)
    submit_button.pack()

    inp_list = [None, None, None, None]

    root.mainloop()
    
    return inp_list


def main():
    num_servers, arrival_rate, service_rate, num_customers = get_input()
    queue = MMcQueue(num_servers, arrival_rate, service_rate, num_customers)
    queue.run()
    draw_graph(queue)
    

if __name__ == "__main__":
    main()