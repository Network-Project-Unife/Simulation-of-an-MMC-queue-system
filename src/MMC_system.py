from math import factorial
from random import random


class MMC_system:
    def __init__(self, servers, arrival_rate, service_rate):
        self.servers = servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.k_state = int(random() * 10)
        self.server_utilization = arrival_rate / (servers * service_rate)
        self.state_0_probability = self._get_state_0_probability()
        self.state_k_probability = self._get_state_k_probability()
        self.queue_probability = self._c_erlang(servers, servers * self.server_utilization)
        self.average_queue_length = self.queue_probability * (self.server_utilization / (1 - self.server_utilization))
        self.average_system_length = ((self.queue_probability / (1 - self.server_utilization)) + servers) * self.server_utilization
        self.average_queue_waiting_time = self.average_queue_length / (servers * service_rate * (1 - self.server_utilization))
        self.average_system_waiting_time = self.average_system_length / (servers * service_rate * (1 - self.server_utilization))

    def _c_erlang(self, c, a):
        num = (a**c / factorial(c)) * (1 / (1 - (a / c)))
        den = 0
        for k in range(c):
            den += (a**k / factorial(k)) + ((a**c / factorial(c)) * (1 / (1 - (a / c))))
        return num / den

    def _get_state_0_probability(self):
        state_zero_probability = 0
        for k in range(self.servers):
            state_zero_probability += ((self.servers * self.server_utilization)**k / factorial(k)) + \
                                ((self.servers * self.server_utilization)**self.servers / factorial(k)) * \
                                (1 / (1 - self.server_utilization))
        return state_zero_probability
    
    def _get_state_k_probability(self):
        if self.k_state <= self.servers:
            return self.state_0_probability * ((self.servers * self.server_utilization)**self.k_state / factorial(self.k_state))
        return self.state_0_probability * (self.servers_utilization**self.k_state / factorial(self.servers))
