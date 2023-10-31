import plotly.graph_objects as go
import plotly.express as px
import re
import statistics
import tkinter as tk
from tkinter import messagebox

from MMcQueue import MMcQueue


def draw_parameters_graph(arrival_rate, service_rate, num_servers):
    fig = go.Figure()
    
    num_sim_server = 30
    sim_servers_x0 = int(arrival_rate // service_rate) + 1
    sim_servers_stop = sim_servers_x0 + num_sim_server
    sim_range = [i for i in range(sim_servers_x0, sim_servers_stop)]
    
    simulations = [MMcQueue(i, arrival_rate, service_rate, 1) for i in sim_range]
    
    fig.add_trace(go.Scatter(
        name="Server utilization",
        x=sim_range,
        y=list(map(lambda s: s.server_utilization, simulations))
    ))
    
    fig.add_trace(go.Scatter(
        name="Probability of 0 customers in the system",
        x=sim_range,
        y=list(map(lambda s: s.state_0_probability, simulations))
    ))
        
    fig.add_trace(go.Scatter(
        name="Average number of customers in the system",
        x=sim_range,
        y=list(map(lambda s: s.average_system_length, simulations))
    ))
    
    fig.add_trace(go.Scatter(
        name="Probability of going to the queue",
        x=sim_range,
        y=list(map(lambda s: s.queue_probability, simulations))
    ))
    
    fig.add_trace(go.Scatter(
        name="Average waiting time in the system",
        x=sim_range,
        y=list(map(lambda s: s.average_system_waiting_time, simulations))
    ))
    
    legend_text = f"""\
Arrival rate:<br>\
{arrival_rate}<br>\
Service rate:<br>\
{service_rate}<br>\
"""

    if num_servers - sim_servers_x0 >= 0 and num_servers - sim_servers_x0 < num_sim_server:
        fig.add_vline(
            num_servers,
            annotation_text="Number of servers chosen", 
            line_dash="dash"
        )
        
    fig.update_layout(
        xaxis=dict(type='category', dtick=1),
        legend=dict(title=legend_text),
    )

    fig.show()


def draw_simulation_graph(queue):
    # Extract the times and number of customers from the customers_history dictionary
    times = list(queue.customers_history.keys())
    customers_in_service = [i["service"] for i in list(queue.customers_history.values())]
    customers_in_queue = [i["queue"] for i in list(queue.customers_history.values())]
    customers_in_system = [i["system"] for i in list(queue.customers_history.values())]

    average_service_length = statistics.mean(customers_in_service)
    average_queue_length = statistics.mean(customers_in_queue)
    average_system_length = statistics.mean(customers_in_system)
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=times,
        y=customers_in_service,
        name='Customers in service'
    ))

    fig.add_trace(go.Bar(
        x=times,
        y=customers_in_queue,
        name='Customers in queue'
    ))

    fig.add_hline(
        y=average_system_length,
        annotation_text="Average customers in system", 
        line_dash="dash"
    )
    
    legend_text = f"""\
Servers:<br>\
{queue.num_servers}<br>\
Arrival rate:<br>\
{queue.arrival_rate}<br>\
Service rate:<br>\
{queue.service_rate}<br>\
Customers:<br>\
{queue.num_customers}<br><br>\
PERFORMANCE MEASURES<br>\
Probaility of 0 customers in the system:<br>\
{queue.state_0_probability * 100}%<br>\
Probability of queue:<br>\
{queue.queue_probability * 100}%<br>\
Average number of customers in service:<br>\
{queue.average_service_length}<br>\
Average number of customers in the queue:<br>\
{queue.average_queue_length}<br>\
Average number of customers in the system:<br>\
{queue.average_system_length}<br>\
Average waiting time in the queue:<br>\
{queue.average_queue_waiting_time}<br>\
Average waiting time in the system:<br>\
{queue.average_system_waiting_time}<br><br>\
SIMULATION PERFORMANCE MEASURES<br>\
Average number of customers in service:<br>\
{average_service_length}<br>\
Average number of customers in the queue:<br>\
{average_queue_length}<br>\
Average number of customers in the system:<br>\
{average_system_length}<br><br>\
"""
    
    fig.update_layout(
        title='Simulation of an M/M/c queue system',
        xaxis=dict(title='Time [s]', type='category', tick0=0, dtick=len(times)-1),
        yaxis=dict(title=f'Number of customers in the system', dtick=1),
        legend=dict(title=f"{legend_text}Customers in the system"),
        barmode="stack",
        bargap=0
    )

    fig.show()


def get_input():
    def validate_input():
        num_servers = entry_servers.get()
        arrival_rate = entry_arrival_rate.get()
        service_rate = entry_service_rate.get()
        num_customers = entry_num_customers.get()
        if "." in num_servers:
            messagebox.showerror("Error", "Number of servers has to be an integer.")
            return
        if "." in num_customers:
            messagebox.showerror("Error", "Number of customers has to be an integer.")
            return
        for inp in [num_servers, arrival_rate, service_rate, num_customers]:
            if not inp:
                messagebox.showerror("Error", "Missing value(s)")
                return
            if not re.match("^([1-9][0-9]*)?(0?\.[0-9]+)?$", inp):
                messagebox.showerror("Error", "Invalid numeric value(s).")
                return
        if (float(arrival_rate) / (int(num_servers) * float(service_rate))) >= 1:
            messagebox.showerror("Error", "Server utilization has to be less than 1 (number of servers * service rate > arrival rate).")
            return
            
        inp_list[0] = int(num_servers)
        inp_list[1] = float(arrival_rate)
        inp_list[2] = float(service_rate)
        inp_list[3] = int(num_customers)
        root.destroy()

    root = tk.Tk()

    root.title("M/M/c queue system simulator")
    root.geometry("400x200")

    # cell for num_servers input
    label_servers = tk.Label(root, text="Insert number of servers:")
    label_servers.pack()
    entry_servers = tk.Entry(root)
    entry_servers.pack()

    # cell for arrival_rate input
    label_arrival_rate = tk.Label(root, text="Insert arrival rate:")
    label_arrival_rate.pack()
    entry_arrival_rate = tk.Entry(root)
    entry_arrival_rate.pack()

    # cell for service_rate input
    label_service_rate = tk.Label(root, text="Insert service rate:")
    label_service_rate.pack()
    entry_service_rate = tk.Entry(root)
    entry_service_rate.pack()

    # cell for num_customers input
    label_num_customers = tk.Label(root, text="Insert number of customers:")
    label_num_customers.pack()
    entry_num_customers = tk.Entry(root)
    entry_num_customers.pack()

    # confirmation button for validating the values in input and starting the program
    submit_button = tk.Button(root, text="Confirm", command=validate_input)
    submit_button.pack()

    inp_list = [None, None, None, None]

    root.mainloop()
    
    return inp_list


def main():
    num_servers, arrival_rate, service_rate, num_customers = get_input()
    queue = MMcQueue(num_servers, arrival_rate, service_rate, num_customers)
    queue.run()
    draw_simulation_graph(queue)
    draw_parameters_graph(arrival_rate, service_rate, num_servers)
    

if __name__ == "__main__":
    main()