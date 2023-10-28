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
        self.queue_probability = self._c_erlang(num_servers, self.server_utilization)
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
            env.process(self._generate_services(env, server, f"Cliente {i+1}"))

    def _generate_services(self, env, server, name):
        arrival_time = env.now
        print(f"{name} arriva al tempo {arrival_time}")
        self.customers_history[arrival_time] = {
            "service": server.count,
            "queue": len(server.queue),
            "system": server.count + len(server.queue)
        }

        with server.request() as req:
            yield req
            
            service_start = env.now
            print(f"{name} inizia il servizio al tempo {service_start}")

            service_duration = random.expovariate(self.service_rate)
            yield env.timeout(service_duration)
    
            service_end = env.now
            print(f"{name} completa il servizio al tempo {service_end}")
            
            time_in_queue = service_start - arrival_time
            time_in_system = service_end - arrival_time
            self.queue_waiting_times.append(time_in_queue)
            self.system_waiting_times.append(time_in_system)
            self.customers_history[arrival_time] = {
                "service": server.count,
                "queue": len(server.queue),
                "system": server.count + len(server.queue)
            }
            
    def _c_erlang(self, c, a):
        den = 0
        for i in range(c):
            den += (((c * a)**i) / math.factorial(i))
        den *= (1 - a) * (math.factorial(c) / ((c * a)**c))
        den += 1
        return 1 / den
        """
        num = ((a**c) / math.factorial(c)) * (1 / (1 - a))
        den = ((a**c) / math.factorial(c)) * (1 / (1 - a))
        for i in range(c):
            den += ((a**i) / math.factorial(i))
        return num / den
        """

    def _get_state_0_probability(self):
        if self.server_utilization >= 1:
            return 0

        state_zero_probability = (((self.num_servers * self.server_utilization)**self.num_servers) \
                                / math.factorial(self.num_servers)) * (1 / (1 - self.server_utilization))
        for i in range(self.num_servers):
            state_zero_probability += ((self.num_servers * self.server_utilization)**i) / math.factorial(i)
        return 1 / state_zero_probability