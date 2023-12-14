import pyvisa as visa


class SampleSettings(object):
    settings: {}

    def __init__(self, freq, delay, width, lead, trail, ampl, sig_type):
        self.settings["f"] = freq
        self.settings["d"] = delay
        self.settings["w"] = width
        self.settings["l"] = lead
        self.settings["t"] = trail
        self.settings["a"] = ampl
        self.settings["type"] = sig_type

    def get_freq(self):
        return str(self.settings["f"])

    def get_delay(self):
        return str(self.settings["d"])

    def get_width(self):
        return str(self.settings["w"])

    def get_lead(self):
        return str(self.settings["l"])

    def get_trail(self):
        return str(self.settings["t"])

    def get_ampl(self):
        return str(self.settings["a"])

    def get_signal_type(self):
        return str(self.settings["type"])


class Sample(object):
    sample: {}

    def __init__(self, edge, ampl, fall, freq):
        self.sample["Edge"] = edge
        self.sample["Amplitude"] = ampl
        self.sample["Frequency"] = freq
        self.sample["Fall"] = fall


class Visa(object):
    # Exceptions
    EXCEPTION_INVALID_RESOURCE = "invalid resource"
    EXCEPTION_INVALID_SIGNAL_SETTINGS = "invalid signal settings"

    # Queries for connect resources
    QUERY_OSCILLOSCOPE = "MSOS204A"
    QUERY_GENERATOR = "811"

    CHANNEL_PROB_CONST = "1.0"

    # Start resource configuration
    RESOURCE_TIMEOUT = 5000
    RESOURCE_QUERY_DELAY = 0.1
    RESOURCE_CHUNCK_SIZE = 100_000
    RESOURCE_TERM_CHARS = ""
    RESOURCE_READ_TERMINATION = "\n"
    RESOURCE_WRITE_TERMINATION = "\0"
    RESOURCE_BAUD_RATE = 115200

    # KEYSIGHT commands
    # STILL DOESN'T USED
    COMMAND_QUERY = "?"
    COMMAND_RESET = "*RST"
    COMMAND_CLEAR = "*CLS"
    COMMAND_ERR_OSCILLOSCOPE = ":SYST:ERR? STR"
    COMMAND_ERR_GENERATOR = ":SYST:ERR?"
    COMMAND_IDN = "*IDN?"
    CHAN_NUM = "CHAN"
    COMMAND_TRIG = ":TRIG"
    COMMAND_MODE = ":MODE"
    COMMAND_EDGE = ":EDGE"
    MODE_EDGE = "EDGE"
    COMMAND_LEV = ":LEV"
    COMMAND_SOUR = ":SOUR"
    COMMAND_CLOP = ":SLOP"
    SLOP_POS = "POS"
    SLOP_NEG = "NEG"
    COMMAND_SWEEP = ":SWE"
    SWEEP_SING = "SING"
    # Fast commands
    SET_TRIG_MODE = COMMAND_TRIG+COMMAND_MODE
    SET_TRIG_EDGE_SOUR = COMMAND_TRIG+COMMAND_EDGE+COMMAND_SOUR+" "+CHAN_NUM
    SET_TRIG_LEV = COMMAND_TRIG+COMMAND_LEV+" "+CHAN_NUM

    # KEYSIGHT signals functions
    PULSE_SIGNAL_TYPE = "PULS"
    SQUARE_SIGNAL_TYPE = "SQU"
    SINE_SIGNAL_TYPE = "SIN"
    RAMP_SIGNAL_TYPE = "RAMP"
    NOISE_SIGNAL_TYPE = "NOIS"
    ARB_SIGNAL_TYPE = "USER"

    # GUI signals functions
    PULSE_BOX_TYPE = "Pulse"
    SQUARE_BOX_TYPE = "Square"
    SINE_BOX_TYPE = "Sine"
    RAMP_BOX_TYPE = "Ramp"
    NOISE_BOX_TYPE = "Noise"
    ARB_BOX_TYPE = "Arb"

    oscilloscope: visa.Resource
    generator: visa.Resource
    rm: visa.ResourceManager

    def __init__(self) -> None:
        self.rm = visa.ResourceManager("@py")

    def send_command(self, resource: visa.Resource, comm: str):
        try:
            resource.write(comm)
        except:
            raise

    def query(self, resource: visa.Resource, comm: str) -> str:
        q = ""
        try:
            q = resource.query(comm).strip()
        except:
            raise
        return q

    def first_configure(self, resource: visa.Resource):
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

    def detect_errors(self, resource: visa.Resource) -> str:
        err_string = ""
        while True:
            str_err = ""
            match resource:
                case self.oscilloscope:
                    str_err = resource.query(
                        self.COMMAND_ERR_OSCILLOSCOPE).strip()
                case self.generator:
                    str_err = resource.query(
                        self.COMMAND_ERR_GENERATOR).strip()

            arr_err = str_err.split(",")

            err_code = 0
            try:
                err_code = int(arr_err[0])
            except Exception as e:
                print("ERROR get error code cause", e)

            if err_code == 0:
                break

            err_string += "Comm err: " + arr_err[1] + "\n"

        if len(err_string) > 1:
            return err_string[:-1]
        return err_string

    def connect_resource(self, address: str, query: str) -> visa.Resource:
        res: visa.Resource
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
        return res

    def connect_osc(self, address: str):
        try:
            self.oscilloscope = self.connect_resource(
                address, self.QUERY_OSCILLOSCOPE)
        except:
            raise

    def connect_gen(self, address: str):
        try:
            self.generator = self.connect_resource(
                address, self.QUERY_GENERATOR)
        except:
            raise

    def signal_type_from_box(self, type: str) -> str:
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

    def reset_resourse(self, resource: visa.Resource):
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

    def prep_oscilloscope(self, chan_numb: int, trig_lvl: int):
        self.send_command(
            self.oscilloscope, f":CHAN{str(chan_numb)}:PROB {self.CHANNEL_PROB_CONST}")
        # self.send_command(self.osc, ":SELECT:CH1 ON")
        # chose trig mode
        self.send_command(self.oscilloscope, ":TRIG:MODE EDGE")
        # trigger settings
        self.send_command(self.oscilloscope,
                          f":TRIG:EDGE:SOUR CHAN{str(chan_numb)}")
        self.send_command(self.oscilloscope,
                          f":TRIG:LEV CHAN{str(chan_numb)}, {str(trig_lvl)}mV")
        self.send_command(self.oscilloscope, ":TRIG:EDGE:SLOP POS")
        # setting type sweep
        self.send_command(self.oscilloscope, ":TRIG:SWE SING")

    def configure_generator_sample(self, data: SampleSettings):
        signal_type = self.signal_type_from_box(data.get_signal_type())

        self.send_command(self.generator, f":FUNC {signal_type}")
        self.send_command(self.generator, f":FREQ {data.get_freq()}Hz")
        self.send_command(self.generator, f":VOLT:HIGH {data.get_ampl()}mV")
        self.send_command(self.generator, f":VOLT:LOW 0V")
        self.send_command(
            self.generator, f":FUNC:{signal_type}:WIDT {data.get_width()}ns")
        self.send_command(
            self.generator, f":FUNC:{signal_type}:DEL {data.get_delay()}s")
        self.send_command(
            self.generator, f":FUNC:{signal_type}:TRAN {data.get_lead()}ns")
        self.send_command(
            self.generator, f":FUNC:{signal_type}:TRAN:TRA {data.get_trail()}ns")

        errors = self.detect_errors(self.generator)

        if errors != "":
            raise Exception(self.EXCEPTION_INVALID_SIGNAL_SETTINGS, errors)

    def measure(self, chan_num: int) -> Sample:
        Edge = self.query(self.oscilloscope,
                          f":MEAS:EDGE? CHAN{str(chan_num)}")
        Amplitude = self.query(
            self.oscilloscope, f":MEAS:VAMP? CHAN{str(chan_num)}")
        Fall = self.query(self.oscilloscope,
                          f":MEAS:FALL? CHAN{str(chan_num)}")
        Frequency = self.query(
            self.oscilloscope, f":MEAS:FREQ? CHAN{str(chan_num)}")

        sample = Sample(edge=Edge, ampl=Amplitude, fall=Fall, freq=Frequency)

        return sample

    def do_sample(self, chan_num: int, generator_settings: SampleSettings, trig_lvl: int):
        self.send_command(self.generator, f":OUTP{str(chan_num)} ON")
        try:
            self.configure_generator_sample(generator_settings)
        except Exception as e:
            if e.args[0] == self.EXCEPTION_INVALID_SIGNAL_SETTINGS:
                print("Bad signal settings")
                return e.args[1]
            return

        self.prep_oscilloscope(chan_num, trig_lvl)
        self.send_command(self.oscilloscope, ":SING")
        self.send_command(self.oscilloscope, f":MEAS:SOUR CHAN{str(chan_num)}")

    def is_resourses_connected(self) -> bool:
        # return self.generator.
        pass

    def res_list(self) -> list[tuple[str, str]]:
        result = []
        buff_res:visa.Resource
        resourses = self.rm.list_resources("TCPIP")
        for res in resourses:
            buff_res = self.rm.open_resource(res)
            buff_res_detail = "no data"
            try:
                buff_res_detail = self.query(buff_res, self.COMMAND_IDN)
            except:
                print(f'Bad access to resourse {res}')
            result.append((res, buff_res_detail))

        return result