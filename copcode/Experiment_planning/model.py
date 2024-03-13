import numpy.random as rn


class GaussGenerator:
    def __init__(self, m, sigma):
        self.m = m
        self.sigma = sigma

    def new(self):
        t = rn.normal(self.m, self.sigma)
        while t < 0:
            t = rn.normal(self.m, self.sigma)
        return t


class ReleyGenerator:
    def __init__(self, sigma):
        self.sigma = sigma

    def new(self):
        t = rn.rayleigh(self.sigma, 1)[0]
        while t < 0:
            t = rn.rayleigh(self.sigma, 1)[0]
        return t


class GenerateRequest:
    def __init__(self, generator, count):
        self.random_generator = generator
        self.num_requests = count
        self.receivers = []
        self.next = 0

    def generate_request(self, time):
        self.num_requests -= 1
        for receiver in self.receivers:
            if receiver.receive_request(time):
                return receiver
        return None

    def delay(self):
        return self.random_generator.new()


class ProcessRequest:
    def __init__(self, generator, max_queue_size=-1):
        self.random_generator = generator
        self.received, self.max_queue, self.processed = 0, max_queue_size, 0
        self.queue = []
        self.next = 0

    def receive_request(self, time):
        if self.max_queue == -1 or self.max_queue > len(self.queue):
            self.queue.append(time)
            self.received += 1
            return True
        return False

    def process_request(self, time, queue_time):
        if len(self.queue) > 0:
            num = self.queue.pop(0)
            queue_time += (time - num)
            self.processed += 1
        return queue_time

    def delay(self):
        return self.random_generator.new()


class Model:
    def __init__(self, generators, processors):
        self.generators = generators
        self.processors = processors
        self.queue_time = 0

    def event_mode(self):
        refusals = 0
        generated_requests = self.generators[0].num_requests

        for generator in self.generators:
            generator.receivers = self.processors
            generator.next = generator.delay()

        for processor in self.processors:
            processor.next = processor.delay()

        blocks = self.generators + self.processors

        while self.processors[0].processed < generated_requests:
            current_time = blocks[0].next
            for block in blocks:
                if 0 < block.next < current_time:
                    current_time = block.next

            for block in blocks:
                if current_time == block.next:
                    if not isinstance(block, ProcessRequest):
                        next_generator = block.generate_request(current_time)
                        if next_generator is not None:
                            next_generator.next = current_time + next_generator.delay()
                        else:
                            refusals += 1
                        block.next = current_time + block.delay()
                    else:
                        self.queue_time = block.process_request(current_time, self.queue_time)
                        if block.queue == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.delay()

        return self.queue_time / generated_requests


def calculate_reley_param(sigma):
    if sigma != 0:
        result = 1.0 / sigma
    else:
        result = sigma
    return result


def calculate_gauss_params(m, dm):
    if m != 0:
        m2 = 1.0 / m
    else:
        m2 = m

    if (m != dm):
        dm2 = (1 / (m - dm) - 1 / (m + dm)) / 2
    else:
        dm2 = 1 / (m + dm) / 2

    return m2, dm2


def convert_factor_to_value(min, max, factor):
    return factor * (max - min) / 2.0 + (max + min) / 2.0


def convert_value_to_factor(min, max, value):
    if max == min:
        return (value - (max + min) / 2.0)
    return (value - (max + min) / 2.0) / ((max - min) / 2.0)


def calculate_b(min, max, values, y, count_experiments):
    b = 0

    for i in range(count_experiments):
        b += values[i] * y[i]
    b /= count_experiments
    return b


def calculate_b_dfe(array_x, min, max, values, y, count_experiments):
    b = 0
    repeats = 0
    for i in range(1, len(array_x[0])):
        k = 0
        for j in range(len(array_x)):
            if (array_x[j][i] == values[j]):
                k += 1
        if (k == len(array_x)):
            repeats += 1

    if repeats == 0:
        repeats = 1

    for i in range(count_experiments):
        b += values[i] * y[i]
    b /= count_experiments
    return b / repeats


def calculate_b_ockp(min, max, values, y, count_experiments):
    b = 0
    for i in range(count_experiments):
        b += values[i] * y[i]

    x = 0
    for v in values:
        x += v*v
    b /= x
    return b


def get_row(params, count):
    i = params[0]
    j = params[1]
    k = params[2]
    if (count == 3):
        return [1, round(i, 5), round(j, 5), round(k, 5), round(i * j, 5),
                round(i * k, 5), round(j * k, 5), round(i * j * k, 5), 0, 0, 0, 0, 0]

    if (count == 4):
        l = params[3]
        return [1, round(i, 5), round(j, 5), round(k, 5), round(l, 5),
                round(i * j, 5), round(i * k, 5), round(i * l, 5),
                round(j * k, 5), round(j * l, 5), round(k * l, 5),
                round(i * j * k, 5), round(i * k * l, 5), round(i * j * l, 5),
                round(j * k * l, 5), round(i * j * k * l, 5), 0, 0, 0, 0, 0]

    if (count == 6):
        l = params[3]
        m = params[4]
        n = params[5]
        return [1, round(i, 5), round(j, 5), round(k, 5), round(l, 5), round(m, 5), round(n, 5),
                round(i * j, 5), round(i * k, 5), round(i * l, 5), round(i * m, 5), round(i * n, 5),
                round(j * k, 5), round(j * l, 5), round(j * m, 5), round(j * n, 5),
                round(k * l, 5), round(k * m, 5), round(k * n, 5),
                round(l * m, 5), round(l * n, 5),
                round(m * n, 5),
                round(i * j * k, 5), round(i * j * l, 5), round(i * j * m, 5), round(i * j * n, 5),
                round(i * k * l, 5), round(i * k * m, 5), round(i * k * n, 5),
                round(i * l * m, 5), round(i * l * n, 5),
                round(i * m * n, 5),
                round(j * k * l, 5), round(j * k * m, 5), round(j * k * n, 5),
                round(j * l * m, 5), round(j * l * n, 5),
                round(j * m * n, 5),
                round(k * l * m, 5), round(k * l * n, 5),
                round(k * m * n, 5),
                round(l * m * n, 5),
                round(i * j * k * l, 5), round(i * j * k * m, 5), round(i * j * k * n, 5),
                round(i * j * l * m, 5), round(i * j * l * n, 5),
                round(i * j * m * n, 5),
                round(i * k * l * m, 5), round(i * k * l * n, 5),
                round(i * k * m * n, 5),
                round(i * l * m * n, 5),
                round(j * k * l * m, 5), round(j * k * l * n, 5),
                round(j * k * m * n, 5),
                round(j * l * m * n, 5),
                round(k * l * m * n, 5),
                round(i * j * k * l * m, 5), round(i * j * k * l * n, 5),
                round(i * j * k * m * n, 5),
                round(i * j * l * m * n, 5),
                round(i * k * l * m * n, 5),
                round(j * k * l * m * n, 5),
                round(i * j * k * l * m * n, 5),
                0, 0, 0, 0, 0]


def get_row_with_s(i, j, k, l, m, n, s):
    return [1, round(i, 5), round(j, 5), round(k, 5), round(l, 5), round(m, 5), round(n, 5),
            round(i * j, 5), round(i * k, 5), round(i * l, 5), round(i * m, 5), round(i * n, 5),
            round(j * k, 5), round(j * l, 5), round(j * m, 5), round(j * n, 5),
            round(k * l, 5), round(k * m, 5), round(k * n, 5),
            round(l * m, 5), round(l * n, 5),
            round(m * n, 5),
            round(i * j * k, 5), round(i * j * l, 5), round(i * j * m, 5), round(i * j * n, 5),
            round(i * k * l, 5), round(i * k * m, 5), round(i * k * n, 5),
            round(i * l * m, 5), round(i * l * n, 5),
            round(i * m * n, 5),
            round(j * k * l, 5), round(j * k * m, 5), round(j * k * n, 5),
            round(j * l * m, 5), round(j * l * n, 5),
            round(j * m * n, 5),
            round(k * l * m, 5), round(k * l * n, 5),
            round(k * m * n, 5),
            round(l * m * n, 5),
            round(i * j * k * l, 5), round(i * j * k * m, 5), round(i * j * k * n, 5),
            round(i * j * l * m, 5), round(i * j * l * n, 5),
            round(i * j * m * n, 5),
            round(i * k * l * m, 5), round(i * k * l * n, 5),
            round(i * k * m * n, 5),
            round(i * l * m * n, 5),
            round(j * k * l * m, 5), round(j * k * l * n, 5),
            round(j * k * m * n, 5),
            round(j * l * m * n, 5),
            round(k * l * m * n, 5),
            round(i * j * k * l * m, 5), round(i * j * k * l * n, 5),
            round(i * j * k * m * n, 5),
            round(i * j * l * m * n, 5),
            round(i * k * l * m * n, 5),
            round(j * k * l * m * n, 5),
            round(i * j * k * l * m * n, 5),
            round(i*i - s, 5), round(j*j - s, 5), round(k*k - s, 5),
            round(l*l - s, 5), round(m*m - s, 5), round(n*n - s, 5),
            0, 0, 0]
