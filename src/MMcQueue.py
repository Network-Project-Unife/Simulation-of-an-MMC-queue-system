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
        self.average_queue_waiting_time = self.average_queue_length / (num_servers * service_rate * (1 - self.server_utilization))
        self.average_system_waiting_time = self.average_system_length / (num_servers * service_rate * (1 - self.server_utilization))
        
        self.customers_history = {}
        self.system_waiting_times = []
        self.queue_waiting_times = []
        
    def run(self):
        env = simpy.Environment()
        server = simpy.Resource(env, capacity=self.num_servers)
        env.process(self._generate_arrivals(env, server))
        env.run()

    def get_state_probability(self, k):
        if k < self.servers:
            return self.state_0_probability * (((self.num_servers * self.server_utilization)**k) / math.factorial(k))
        return self.state_0_probability * (((self.num_servers * self.servers_utilization)**k) \
            * (self.num_servers**(self.num_servers - k))) / math.factorial(self.num_servers)

    def _generate_arrivals(self, env, server):
        for i in range(self.num_customers):
            interarrival_time = random.expovariate(self.arrival_rate)
            yield env.timeout(interarrival_time)
            env.process(self._generate_services(env, server))

    def _generate_services(self, env, server):
        with server.request() as req:
            yield req
            service_start = env.now
            self.customers_history[service_start] = {
                "service": server.count,
                "queue": len(server.queue),
                "system": server.count + len(server.queue)
            }
            
            service_duration = random.expovariate(self.service_rate)
            yield env.timeout(service_duration)
            service_end = env.now
            self.customers_history[service_end] = {
                "service": server.count,
                "queue": len(server.queue),
                "system": server.count + len(server.queue)
            }

            time_in_queue = service_end - service_start  #TODO
            time_in_system = service_end - service_start
            self.queue_waiting_times.append(time_in_queue)
            self.system_waiting_times.append(time_in_system)
            

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