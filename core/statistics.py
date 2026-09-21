import time


class Statistics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        self.response_times = []

        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def finish(self):
        self.end_time = time.perf_counter()

    def add_success(self, response_time):
        self.total_requests += 1
        self.successful_requests += 1
        self.response_times.append(response_time)

    def add_failure(self, response_time):
        self.total_requests += 1
        self.failed_requests += 1
        self.response_times.append(response_time)

    @property
    def duration(self):
        if self.start_time is None:
            return 0

        end = self.end_time or time.perf_counter()
        return end - self.start_time

    @property
    def average_response_time(self):
        if not self.response_times:
            return 0

        return sum(self.response_times) / len(self.response_times)

    @property
    def minimum_response_time(self):
        if not self.response_times:
            return 0

        return min(self.response_times)

    @property
    def maximum_response_time(self):
        if not self.response_times:
            return 0

        return max(self.response_times)

    @property
    def success_rate(self):
        if self.total_requests == 0:
            return 0

        return (self.successful_requests / self.total_requests) * 100

    @property
    def requests_per_second(self):
        if self.duration <= 0:
            return 0

        return self.total_requests / self.duration

    def get_report(self):
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.success_rate,
            "average_response_time": self.average_response_time,
            "minimum_response_time": self.minimum_response_time,
            "maximum_response_time": self.maximum_response_time,
            "requests_per_second": self.requests_per_second,
            "duration": self.duration,
        }
