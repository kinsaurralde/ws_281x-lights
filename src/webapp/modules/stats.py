import time


class Stats:
    def __init__(self) -> None:
        self.ready = False
        self.metrics = {}

    def createMetrics(self, metric_name_list) -> None:
        if not self.ready:
            for metric in metric_name_list:
                self.metrics[metric] = {}
            self.ready = True

    def add(self, key, timestamp, metric_values) -> None:
        for metric in metric_values:
            if metric not in self.metrics:
                continue
            if key not in self.metrics[metric]:
                self.metrics[metric][key] = []
            self.metrics[metric][key].append((timestamp, metric_values[metric]))

    def getRecent(self, metric):
        result = {}
        if metric not in self.metrics:
            return result
        for ip in self.metrics[metric]:
            values = self.metrics[metric][ip]
            if len(values) > 0:
                result[ip] = values[-1]
        return result

    def getMetric(self, metric):
        result = {}
        if metric not in self.metrics:
            return result
        for key in self.metrics[metric]:
            result[key] = {"x": [], "y": [], "name": key}
            for timestamp, value in self.metrics[metric][key]:
                result[key]["x"].append(timestamp)
                result[key]["y"].append(value)
        return result

    def filterRecentNSecs(self, metric, n, min_size=60):
        if metric not in self.metrics:
            return {}
        oldest_timestamp = int(time.time() * 1000) - n * 1000
        result = {}
        for key in self.metrics[metric]:
            result[key] = []
            for item in reversed(self.metrics[metric][key]):
                if (len(result[key]) < min_size) or (item[0] > oldest_timestamp):
                    result[key].insert(0, item)
        self.metrics[metric] = result
        return self.getMetric(metric)
