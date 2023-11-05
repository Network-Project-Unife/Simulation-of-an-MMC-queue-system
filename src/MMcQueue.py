import math
import random
import simpy


class MMcQueue:
    def __init__(self, num_servers, arrival_rate, service_rate, num_customers):
        self.num_servers = num_servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_customers = num_customers

        self.server_utilization = arrival_rate / (num_servers * service_rate)
        self.state_0_probability = self._get_state_0_probability()
        self.queue_probability = self._c_erlang(num_servers, num_servers * self.server_utilization)
        self.average_queue_length = self.queue_probability * (self.server_utilization / (1 - self.server_utilization))
        self.average_service_length =  num_servers * self.server_utilization
        self.average_system_length = self.average_queue_length + self.average_service_length
        self.average_queue_waiting_time = self.queue_probability / (self.num_servers * self.service_rate * (1 - self.server_utilization))
        self.average_system_waiting_time = (self.queue_probability + (self.num_servers * (1 - self.server_utilization))) / (self.num_servers * self.service_rate * (1 - self.server_utilization))
        
        self.customers_history = {}
        self.simulation_state_0_probability = None
        self.simulation_queue_probability = None
        self.simulation_queue_waiting_times = []
        self.simulation_service_waiting_times = []
        self.simulation_system_waiting_times = []
        
        self._store_customers_in_system(0, 0, 0)
        
    def run(self):
        env = simpy.Environment()
        server = simpy.Resource(env, capacity=self.num_servers)
        env.process(self._generate_arrivals(env, server))
        env.run()
        self.simulation_state_0_probability = self._get_simulation_state_0_probability()
        self.simulation_queue_probability = self._get_simulation_queue_probability()

    def _generate_arrivals(self, env, server):
        for i in range(self.num_customers):
            last_arrival = env.now
            interarrival_time = random.expovariate(self.arrival_rate)
            yield env.timeout(interarrival_time)
            env.process(self._generate_services(env, server, last_arrival))            

    def _generate_services(self, env, server, last_arrival):
        while True:
            virtual_service = random.expovariate(self.service_rate)
            if virtual_service > env.now - last_arrival: 
                break
            self._store_customers_in_system(last_arrival + virtual_service, server.count, len(server.queue))
            last_arrival += virtual_service

        arrival_time = env.now
        with server.request() as req:
            yield req
            service_duration = random.expovariate(self.service_rate)
            yield env.timeout(service_duration)
            if len(server.queue) > 0:
                self.simulation_queue_waiting_times.append(env.now - arrival_time)
            else:
                self.simulation_service_waiting_times.append(env.now - arrival_time)
                self.simulation_queue_waiting_times.append(0)
            self.simulation_system_waiting_times.append(env.now - arrival_time)
            self._store_customers_in_system(env.now, server.count, len(server.queue))
            
    def _store_customers_in_system(self, time, service, queue):
        self.customers_history[time] = {
            "service": service,
            "queue": queue,
            "system": service + queue
        }

    def _c_erlang(self, c, a):
        l = ((a**c) / math.factorial(c)) * (1 / (1 - (a / c)))
        sum_ = 0
        for i in range(c):
            sum_ += (a**i) / math.factorial(i)
        return l / (sum_ + l)

    def _get_state_0_probability(self):
        state_zero_probability = (((self.num_servers * self.server_utilization)**self.num_servers) \
                                / math.factorial(self.num_servers)) * (1 / (1 - self.server_utilization))
        for i in range(self.num_servers):
            state_zero_probability += ((self.num_servers * self.server_utilization)**i) / math.factorial(i)
        return 1 / state_zero_probability

    def _get_simulation_state_0_probability(self):
        return len([k for k in self.customers_history if self.customers_history[k]["system"] == 0]) / len(self.customers_history)
        
    def _get_simulation_queue_probability(self):
        return len([k for k in self.customers_history if self.customers_history[k]["service"] == self.num_servers]) / len(self.customers_history)
    
    def get_state_probability(self, k):
        if k < self.num_servers:
            return self.state_0_probability * (((self.num_servers * self.server_utilization)**k) / math.factorial(k))
        return self.state_0_probability * (((self.num_servers * self.server_utilization)**k) \
            * (self.num_servers**(self.num_servers - k))) / math.factorial(self.num_servers)
