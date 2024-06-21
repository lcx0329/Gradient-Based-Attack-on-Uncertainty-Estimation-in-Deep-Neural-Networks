import time

class Timer:
    def __init__(self, task=None, verbose=True, time_unit='s', decimal_places=3):
        self.start_time = None
        self.elapsed_time = None
        if task is None:
            self.task = "Undefined"
        else:
            self.task = task
        self.unit = time_unit
        self.decimal_places = decimal_places
        self.verbose = verbose
    
    def __enter__(self):
        self.start_time = time.time()
        if self.verbose:
            print(f"Task [{str(self.task)}] started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_time = time.time() - self.start_time
        if self.verbose:
            print(f"Task [{str(self.task)}] elapsed for [{self.get_elapsed_time()} {self.unit}]")
    
    def get_elapsed_time(self):
        if self.unit == 's':
            return round(time.time() - self.start_time, 3)
        elif self.unit == 'ms':
            return round((time.time() - self.start_time) * 1000, 3)
        else:
            raise ValueError(f"Invalid unit '{self.unit}'")
