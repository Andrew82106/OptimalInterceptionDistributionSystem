import os

NameOfRoot = "mutiAGVallocator"


class config:
    def __init__(self):
        self.Root = str(os.getcwd())[:str(os.getcwd()).find(NameOfRoot)] + NameOfRoot
        self.utils = os.path.join(self.Root, "codelogs", "utils")
        self.DataLogs = os.path.join(self.Root, "datalogs", "release", "taxi_log_2008_by_id")
        self.RouteSum = os.path.join(self.DataLogs, "轨迹汇总.json")
        self.RouteSumMini = os.path.join(self.DataLogs, "轨迹汇总(Mini).json")
        self.latRange = (39.636556, 40.224357)
        self.lngRange = (116.016776, 116.858452)
        self.RoutePKL = os.path.join(self.DataLogs, "Markov.pkl")


if __name__ == '__main__':
    x = config()
    print(x.Root)
    print(x.utils)
    print(x.RoutePKL)