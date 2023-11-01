import plotly.graph_objects as go
import plotly.express as px
import re
import statistics
import tkinter as tk
from tkinter import messagebox

from MMcQueue import MMcQueue


NUM_SIM_SERVERS = 30
DECIMAL_DIGITS = 3
LINE_WIDTH = 5
MARKER_SIZE = 10
MARKER_BORDER_WIDTH = 2


def draw_pk_graph(queue):
    pks = []
    percent = 0.0
    while percent < 99.99:
        k_probability = queue.get_state_probability(len(pks)) * 100
        pks.append(k_probability)
        percent += k_probability

    fig = go.Figure()
    
    hovertemplate = "<b>Probability of %{x} customers</b>:<br>%{y:g}%"
    
    fig.add_trace(go.Scatter(
        name="Probability of k customers in the system",
        x=[i for i in range(len(pks))],
        y=pks,
        mode="lines+markers",
        line=dict(
            width=LINE_WIDTH
        ),
        marker=dict(
            size=MARKER_SIZE,
            line=dict(
                width=MARKER_BORDER_WIDTH
            )
        )
    ))
    
    legend_text = f"""\
<b>Servers</b>: {queue.num_servers}<br>\
<b>Arrival rate</b>: {queue.arrival_rate}<br>\
<b>Service rate</b>: {queue.service_rate}<br>\
"""

    fig.update_traces(hovertemplate=hovertemplate)
    
    fig.update_layout(
        title="Probability of k customers in the system",
        xaxis=dict(title="Number of customers", type='category', dtick=1),
        yaxis=dict(title="Probability %"),
        legend=dict(title=legend_text),
        showlegend=True,
        hovermode="x"
    )

    fig.show()


def draw_waiting_time_graph(arrival_rate, service_rate, num_servers):
    sim_range = [i for i in range(1, NUM_SIM_SERVERS + 1)]
    
    hoverdata= []
    simulations = []
    server_utilization = arrival_rate / (service_rate * num_servers)
    for i_num_servers in sim_range:
        i_service_rate = arrival_rate / (i_num_servers * server_utilization)
        q = MMcQueue(i_num_servers, arrival_rate, i_service_rate, 1)
        simulations.append(q)
        hoverdata.append(q.service_rate)
        
    fig = go.Figure()
    
    hovertemplate = "<b>Arrival rate</b>: " + str(arrival_rate) + \
                    "<br><b>Service rate</b>: %{customdata:g}" + \
                    "<br><b>Servers</b>: %{x}" + \
                    "<br><b>Value</b>: %{y:g}"
        
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
    
    fig.add_vline(
        num_servers - 1,
        annotation_text="Number of servers chosen", 
        line_dash="dash"
    )
    
    fig.update_traces(
        mode="lines+markers",
        line=dict(
            width=LINE_WIDTH
        ),
        marker=dict(
            size=MARKER_SIZE,
            line=dict(
                width=MARKER_BORDER_WIDTH
            )
        ),
        customdata=hoverdata,
        hovertemplate=hovertemplate
    )
    
    legend_text = f"<b>Arrival rate</b>: {arrival_rate}<br><b>Server utilization</b>: {round(server_utilization, 3)}<br>"
    
    fig.update_layout(
        title="Average system waiting times of an M/M/c system (constant server utilization)",
        xaxis=dict(title="Number of servers", type='category', dtick=1),
        hovermode="x",
        legend=dict(title=legend_text)
    )

    fig.show()


def draw_parameters_graph(arrival_rate, service_rate, num_servers):
    fig = go.Figure()
    
    hovertemplate = "<b>Value</b>: %{y:g}"
    
    sim_servers_x0 = int(arrival_rate // service_rate) + 1
    sim_servers_stop = sim_servers_x0 + NUM_SIM_SERVERS
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
<b>Arrival rate</b>: {arrival_rate}<br>\
<b>Service rate</b>: {service_rate}<br>\
"""

    if num_servers - sim_servers_x0 >= 0 and num_servers - sim_servers_x0 < NUM_SIM_SERVERS:
        fig.add_vline(
            num_servers - sim_servers_x0,
            annotation_text="Number of servers chosen", 
            line_dash="dash"
        )
        
    fig.update_traces(
        mode="lines+markers",
        line=dict(
            width=LINE_WIDTH
        ),
        marker=dict(
            size=MARKER_SIZE,
            line=dict(
                width=MARKER_BORDER_WIDTH
            )
        ),
        hovertemplate=hovertemplate
    )
        
    fig.update_layout(
        title="Performance measures of an M/M/c system",
        xaxis=dict(title="Number of servers", type='category', dtick=1),
        legend=dict(title=legend_text),
        hovermode="x"
    )

    fig.show()


def draw_simulation_graph(queue):
    times = list(queue.customers_history.keys())
    customers_in_service = [i["service"] for i in list(queue.customers_history.values())]
    customers_in_queue = [i["queue"] for i in list(queue.customers_history.values())]
    customers_in_system = [i["system"] for i in list(queue.customers_history.values())]

    average_service_length = statistics.mean(customers_in_service)
    average_queue_length = statistics.mean(customers_in_queue)
    average_system_length = statistics.mean(customers_in_system)
    
    fig = go.Figure()
    
    hovertemplate = "<b>Time</b>: %{x:g}<br><b>Customers in the system</b>: %{y}"

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
<b>Servers</b>: {queue.num_servers}<br>\
<b>Arrival rate</b>: {queue.arrival_rate}<br>\
<b>Service rate</b>: {queue.service_rate}<br>\
<b>Customers</b>: {queue.num_customers}<br><br>\
<b>PERFORMANCE MEASURES</b><br>\
Probability of 0 customers in the system:<br>\
{round(queue.state_0_probability * 100, DECIMAL_DIGITS)}%<br>\
Probability of queue:<br>\
{round(queue.queue_probability * 100, DECIMAL_DIGITS)}%<br>\
Average number of customers in service:<br>\
{round(queue.average_service_length, DECIMAL_DIGITS)}<br>\
Average number of customers in the queue:<br>\
{round(queue.average_queue_length, DECIMAL_DIGITS)}<br>\
Average number of customers in the system:<br>\
{round(queue.average_system_length, DECIMAL_DIGITS)}<br>\
Average waiting time in the queue:<br>\
{round(queue.average_queue_waiting_time, DECIMAL_DIGITS)}<br>\
Average waiting time in the system:<br>\
{round(queue.average_system_waiting_time, DECIMAL_DIGITS)}<br><br>\
<b>SIMULATION PERFORMANCE MEASURES</b><br>\
Average number of customers in service:<br>\
{round(average_service_length, DECIMAL_DIGITS)}<br>\
Average number of customers in the queue:<br>\
{round(average_queue_length, DECIMAL_DIGITS)}<br>\
Average number of customers in the system:<br>\
{round(average_system_length, DECIMAL_DIGITS)}<br><br>\
"""

    fig.update_traces(hovertemplate=hovertemplate)
    
    fig.update_layout(
        title='Simulation of an M/M/c queue system',
        xaxis=dict(title='Time [s]', type='category', tick0=0, dtick=len(times)-1, tickformat=f".{DECIMAL_DIGITS}%"),
        yaxis=dict(title=f'Number of customers in the system', dtick=1),
        legend=dict(title=f"{legend_text}<b>Customers in the system</b>"),
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
    draw_pk_graph(queue)
    draw_parameters_graph(arrival_rate, service_rate, num_servers)
    draw_waiting_time_graph(arrival_rate, service_rate, num_servers)
    

if __name__ == "__main__":
    main()