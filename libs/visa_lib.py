import pyvisa as visa

class Visa(object):
    # Exceptions
    EXCEPTION_INVALID_RESOURCE = "invalid resource"

    # Queries for connect resources
    QUERY_OSCILLOSCOPE = "MSOS204A"
    QUERY_GENERATOR = "811"

    # Start resource configuration
    RESOURCE_TIMEOUT = 5000
    RESOURCE_QUERY_DELAY = 0.1
    RESOURCE_CHUNCK_SIZE = 100_000
    RESOURCE_TERM_CHARS = ""
    RESOURCE_READ_TERMINATION = "\n"
    RESOURCE_WRITE_TERMINATION = "\0"
    RESOURCE_BAUD_RATE = 115200

    # KEYSIGHT commands
    COMMAND_RESET = "*RST"
    COMMAND_CLEAR = "*CLS"
    COMMAND_ERR_OSCILLOSCOPE = ":SYST:ERR? STR"
    COMMAND_ERR_GENERATOR = ":SYST:ERR?"
    COMMAND_IDN = "*IDN?"
    COMMAND_CHAN_NUM = "CHAN"
    
    COMMAND_TRIG = ":TRIG"
    COMMAND_TRIG_MODE = ":MODE"
    COMMAND_TRIG_MODE = "EDGE"
    COMMAND_
    COMMAND_

    # KEYSIGHT signals functions
    PULSE_SIGNAL_TYPE = "PULS"
    SQUARE_SIGNAL_TYPE = "SQU"
    SINE_SIGNAL_TYPE = "SIN"
    RAMP_SIGNAL_TYPE = "RAMP"
    NOISE_SIGNAL_TYPE = "NOIS"
    ARB_SIGNAL_TYPE = "USER"

    # GUI signals functions
    PULSE_BOX_TYPE = "PULSE"
    SQUARE_BOX_TYPE = "SQUARE"
    SINE_BOX_TYPE = "SINE"
    RAMP_BOX_TYPE = "RAMP"
    NOISE_BOX_TYPE = "NOISE"
    ARB_BOX_TYPE = "ARB"
    
    oscilloscope:visa.Resource
    generator:visa.Resource
    rm:visa.ResourceManager

    def __init__(self) -> None:
        rm = visa.ResourceManager("@py")

    def send_command(self, resource:visa.Resource , comm:str):
        try:
            resource.write(comm)
        except:
            raise

    def query(self, resource:visa.Resource , comm:str) -> str:
        q = ""
        try:
            q = resource.query(comm).strip()
        except:
            raise
        return q

    def first_configure(self, resource:visa.Resource):
        resource.clear()
        resource.timeout = self.RESOURCE_TIMEOUT
        resource.query_delay = self.RESOURCE_QUERY_DELAY
        resource.chunk_size = self.RESOURCE_CHUNCK_SIZE
        resource.term_chars = self.RESOURCE_TERM_CHARS
        resource.read_termination = self.RESOURCE_READ_TERMINATION
        resource.write_termination = self.RESOURCE_WRITE_TERMINATION
        resource.baud_rate = self.RESOURCE_BAUD_RATE
        self.send_command(resource, self.COMMAND_CLEAR)
        self.send_command(resource, self.COMMAND_RESET)

    def detect_errors(self, resource:visa.Resource)->str:
        err_string = ""
        while True:
            str_err = ""
            match resource:
                case self.oscilloscope:
                    str_err = resource.query(self.COMMAND_ERR_OSCILLOSCOPE).strip()
                case self.generator:
                    str_err = resource.query(self.COMMAND_ERR_GENERATOR).strip()

            arr_err = str_err.split(",")

            err_code = 0
            try:
                err_code = int(arr_err[0])
            except Exception as e:
                print("ERROR get error code cause", e)
            
            if err_code == 0:
                break

            err_string += "Comm err: "+ arr_err[1] + "\n"

        if len(err_string)>1:
            return err_string[:-1]
        return err_string
    
    def connect_resource(self, address:str, query:str)->visa.Resource:
        res:visa.Resource
        try:
            res = self.rm.open_resource(address)
        except:
            raise
        
        idn = self.query(res, self.COMMAND_IDN)
        if idn.find(query) == -1:
            res.close()
            print(f"Invalid resource, need {query}, get {idn}")
            raise Exception(self.EXCEPTION_INVALID_RESOURCE)

        self.first_configure(res)

    def connect_osc(self, address:str):
        try:
            self.oscilloscope = self.connect_resource(address, self.QUERY_OSCILLOSCOPE)
        except:
            raise

    def connect_gen(self, address:str):
        try:
            self.generator = self.connect_resource(address, self.QUERY_GENERATOR)
        except:
            raise
        
    def signal_type_from_box(self, type:str)->str:
        match type:
            case self.PULSE_BOX_TYPE:
                return self.PULSE_SIGNAL_TYPE
            case self.SQUARE_BOX_TYPE:
                return self.SQUARE_SIGNAL_TYPE
            case self.SINE_BOX_TYPE:
                return self.SINE_SIGNAL_TYPE
            case self.RAMP_BOX_TYPE:
                return self.RAMP_SIGNAL_TYPE
            case self.NOISE_BOX_TYPE:
                return self.NOISE_SIGNAL_TYPE
            case self.ARB_BOX_TYPE:
                return self.ARB_SIGNAL_TYPE
            
    def reset_resourse(self, resource:visa.Resource):
        self.send_command(resource, self.COMMAND_CLEAR)
        self.send_command(resource, self.COMMAND_RESET)
        try:
            resource.close()
        except:
            raise

    def reset_oscilloscope(self):
        self.reset_resourse(self.oscilloscope)

    def reset_generator(self):
        self.reset_resourse(self.generator)

"""
Тут надо сделать класс для стенда с функциями только для UI
Чтобы сгенерированный UI просто подбрасывался этим классом
"""