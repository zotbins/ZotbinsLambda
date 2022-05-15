# Custom Exceptions File

class BinNotFoundException(Exception):
    '''
    BinNotFoundException is raised when bin doesn't exist
    '''
    def __init__(self):
        self.err_msg = "Bin not found!"
        self.err_code = 404

class InvalidMethodException(Exception):
    '''
    '''
    def __init__(self):
        self.err_msg = ""
        self.err_code = 405

class InvalidSensorIdException(Exception):
    '''
    InvalidSensorIdException is raised when none of the metrics are assigned to a sensor with the requested 
    sensor id.
    '''
    def __init__(self):
        self.err_msg = "No metrics found due to invalid sensor id"
        self.err_code = 400

class InvalidRestMethodException(Exception):
    '''
    The InvalidRestMethodException is raised when a valid endpoint is called but with an invalid rest method type. 
    '''
    def __init__(self):
        self.err_msg = "Endpoint does not have corresponding rest method type"
        self.err_code = 405

class InvalidTimestampOrderException(Exception):
    '''
    The InvalidTimestampOrderException is raised when the start timestamp occurs after the end timestamp. 
    '''
    def __init__(self):
        self.err_msg = "Start timestamp occurs after end timestamp"
        self.err_code = 404