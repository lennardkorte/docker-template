
import sys

class Logger(object):
    def __enter__(self):
        pass
    
    def __exit__(self, exception_type, exception_value, traceback):
        pass
    
    def __init__(self, file_name, mode):
        self.file = open(file_name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
        
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
        
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        
    def flush(self):
        self.file.flush()
        
    @staticmethod
    def print_section_line():
        print('\n--------------------------------------------------------')