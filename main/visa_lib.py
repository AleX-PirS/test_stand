from numpy import mat
import pyvisa as visa

from pkg import Channel, GeneratorSample, OscilloscopeData

# Queries for connect resources
QUERY_OSCILLOSCOPE = "MSOS204A"
QUERY_GENERATOR = "811"

CHANNEL_PROB_CONST = "1.0"

# Start resource configuration
RESOURCE_TIMEOUT = 1500
RESOURCE_QUERY_DELAY = 0.1
RESOURCE_CHUNCK_SIZE = 100_000
RESOURCE_TERM_CHARS = ""
RESOURCE_READ_TERMINATION = "\n"
RESOURCE_WRITE_TERMINATION = "\0"
RESOURCE_BAUD_RATE = 115200

# KEYSIGHT most common commands
COMMAND_QUERY = "?"
COMMAND_RESET = "*RST"
COMMAND_CLEAR = "*CLS"
COMMAND_ERR_OSCILLOSCOPE = ":SYST:ERR? STR"
COMMAND_ERR_GENERATOR = ":SYST:ERR?"
COMMAND_IDN = "*IDN?"

# class Sample(object):
#     sample: {}

#     def __init__(self, edge, ampl, fall, freq):
#         self.sample["Edge"] = edge
#         self.sample["Amplitude"] = ampl
#         self.sample["Frequency"] = freq
#         self.sample["Fall"] = fall


class Visa(object):
    def __init__(self) -> None:
        self.rm = visa.ResourceManager("@py")
        self.oscilloscope = visa.Resource(self.rm, "oscilloscope")
        self.generator = visa.Resource(self.rm, "generator")

    def send_command(self, resource: visa.Resource, comm: str):
        resource.write(comm)

    def query(self, resource: visa.Resource, comm: str) -> str:
        q = ""
        q = resource.query(comm).strip()
        return q

    def first_configure(self, resource: visa.Resource):
        resource.clear()
        resource.timeout = RESOURCE_TIMEOUT
        resource.query_delay = RESOURCE_QUERY_DELAY
        resource.chunk_size = RESOURCE_CHUNCK_SIZE
        resource.term_chars = RESOURCE_TERM_CHARS
        resource.read_termination = RESOURCE_READ_TERMINATION
        resource.write_termination = RESOURCE_WRITE_TERMINATION
        resource.baud_rate = RESOURCE_BAUD_RATE
        self.send_command(resource, COMMAND_CLEAR)
        self.send_command(resource, COMMAND_RESET)

    def detect_errors(self, resource: visa.Resource) -> str:
        err_string = ""
        while True:
            str_err = ""
            match resource:
                case self.oscilloscope:
                    str_err = resource.query(COMMAND_ERR_OSCILLOSCOPE).strip()
                case self.generator:
                    str_err = resource.query(COMMAND_ERR_GENERATOR).strip()

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
            if err_string[:-1] != "":
                raise Exception(err_string[:-1])

    def connect_resource(self, address: str, query: str) -> visa.Resource:
        res: visa.Resource
        res = self.rm.open_resource(address)

        idn = self.query(res, COMMAND_IDN)
        if idn.find(query) == -1:
            res.close()
            print(f"Invalid resource, need {query}, get {idn}")
            raise Exception("Invalid resource")

        self.first_configure(res)
        return res

    def connect_osc(self, address: str):
        self.oscilloscope = self.connect_resource(address, QUERY_OSCILLOSCOPE)
        self.clear_resource(self.oscilloscope)
        self.send_command(self.oscilloscope, ":WAV:STR ON")
        self.send_command(self.oscilloscope, ":ACQ:COMP 100")
        self.send_command(self.oscilloscope, ":ACQ:POIN:AUTO ON")
        self.send_command(self.oscilloscope, ":ACQ:MODE HRES")
        self.detect_errors(self.oscilloscope)
        return

    def connect_gen(self, address: str):
        self.generator = self.connect_resource(address, QUERY_GENERATOR)
        self.clear_resource(self.generator)
        self.detect_errors(self.generator)
        return

    def clear_resource(self, resource):
        self.send_command(resource, COMMAND_CLEAR)
        self.send_command(resource, COMMAND_RESET)
        return

    def reset_resource(self, resource: visa.Resource):
        self.clear_resource(resource)
        resource.close()
        return

    def reset_oscilloscope(self):
        self.v2_oscilloscope_ping()
        self.reset_resource(self.oscilloscope)
        return

    def reset_generator(self):
        self.v2_generator_ping()
        self.reset_resource(self.generator)
        return

    def v2_meas_osc_data(self, channels:list[Channel]):
        self.v2_oscilloscope_ping()
        sample = {}
        for ch in channels:
            edge = self.query(self.oscilloscope, f":MEAS:EDGE? CHAN{ch.index}")
            amplitude = self.query(self.oscilloscope, f":MEAS:VAMP? CHAN{ch.index}")
            fall = self.query(self.oscilloscope, f":MEAS:FALL? CHAN{ch.index}")

            sample[ch.index] = {'ampl':amplitude, 'edge':edge, 'fall':fall}

        self.detect_errors(self.oscilloscope)
        return sample

    def resource_list(self) -> list[tuple[str, str]]:
        result = []
        buff_res:visa.Resource
        resourses = self.rm.list_resources("TCPIP")
        for res in resourses:
            buff_res = self.rm.open_resource(res)
            buff_res_detail = "no data"
            try:
                buff_res_detail = self.query(buff_res, COMMAND_IDN)
            except:
                print(f'Bad access to resourse {res}')
            result.append((res, buff_res_detail))

        return result
    
    def v2_configurate_ADC_sample(self, config:GeneratorSample):
        self.v2_generator_ping()
        self.send_command(self.generator, f":FUNC USER")
        self.send_command(self.generator, f":FUNC:USER CONST")
        self.send_command(self.generator, f":FREQ {config.freq}")
        
        self.send_command(self.generator, f":ARM:SOUR IMM")

        self.send_command(self.generator, f":VOLT:OFFS {config.offset}")
        self.send_command(self.generator, f":VOLT {config.ampl}")

        self.detect_errors(self.generator)

    def v2_configurate_generator_sample(self, config:GeneratorSample):
        self.v2_generator_ping()
        # :OUTPut[1|2]:IMPedance:EXTernal
        self.send_command(self.generator, f":FUNC {config.signal_type}")
        self.send_command(self.generator, f":FREQ {config.freq}")
        if config.is_triggered:
            self.send_command(self.generator, f":ARM:SOUR EXT")
            self.send_command(self.generator, f":ARM:LEV {config.trig_lvl}")
            self.send_command(self.generator, f":ARM:SENS LEV")
        else:
            self.send_command(self.generator, f":ARM:SOUR IMM")

        match config.signal_type:
            case "PULS":
                self.send_command(self.generator, f":FUNC:{config.signal_type}:WIDT {config.width}")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:TRAN {config.lead}")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:TRAN:TRA {config.trail}")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:DEL {config.delay}")
                self.send_command(self.generator, f":VOLT:HIGH {float(config.ampl)+float(config.offset)}")
                self.send_command(self.generator, f":VOLT:LOW {float(config.offset)}")
            case "SQU" | "RAMP" | "SIN" | "USER":
                self.send_command(self.generator, f":VOLT:OFFS {config.offset}")
                self.send_command(self.generator, f":VOLT {config.ampl}")
                pass
            case "NOIS":
                self.send_command(self.generator, f":VOLT:OFFS {config.offset}")
                self.send_command(self.generator, f":VOLT {config.ampl}")
                pass

        self.detect_errors(self.generator)
    
    def v2_toggle_out1(self):
        self.v2_generator_ping()
        match self.query(self.generator, f":OUTP1?"):
            case "OFF" | "0":
                self.send_command(self.generator, ":OUTP1 ON")
            case "ON" | "1":
                self.send_command(self.generator, ":OUTP1 OFF")
        self.detect_errors(self.generator)

    def v2_toggle_not_out1(self):
        self.v2_generator_ping()
        match self.query(self.generator, f":OUTP1:COMP?"):
            case "OFF" | "0":
                self.send_command(self.generator, ":OUTP1:COMP ON")
            case "ON" | "1":
                self.send_command(self.generator, ":OUTP1:COMP OFF")
        self.detect_errors(self.generator)

    def v2_on_out1(self, out_index):
        self.v2_generator_ping()
        match out_index:
            case 0:
                self.send_command(self.generator, f":OUTP1 ON")
            case 1:
                self.send_command(self.generator, f":OUTP1:COMP ON")
            case _:
                self.send_command(self.generator, f":OUTP1 ON")
                self.send_command(self.generator, f":OUTP1:COMP ON")
        self.detect_errors(self.generator)
    
    def v2_off_all_out1(self):
        self.v2_generator_ping()
        self.send_command(self.generator, f":OUTP1 OFF")
        self.send_command(self.generator, f":OUTP1:COMP OFF")
        self.detect_errors(self.generator)

    def v2_configurate_oscilloscope_scenario(self, channels:list[Channel], trig_src, trig_lvl, tim_scale, polarity=1, avg_cnt=1):
        self.v2_oscilloscope_ping()

        if avg_cnt > 1:
            self.send_command(self.oscilloscope, f":ACQ:AVER:COUN {avg_cnt}")
            self.send_command(self.oscilloscope, f":ACQ:AVER ON")

        for i in range(1, 5):
            self.send_command(self.oscilloscope, f":CHAN{i} OFF")
        for ch in channels:
            self.send_command(self.oscilloscope, f":CHAN{ch.index} ON")
            self.send_command(self.oscilloscope, f":CHAN{ch.index}:INP AC")
            if ch.index == 1:
                self.send_command(self.oscilloscope, f":CHAN{ch.index}:INP DC50")


        # trigger settings
        self.send_command(self.oscilloscope, ":TRIG:MODE EDGE")
        self.send_command(self.oscilloscope, f":TRIG:EDGE:SOUR CHAN{trig_src}")
        self.send_command(self.oscilloscope, f":TRIG:LEV CHAN{trig_src}, {trig_lvl}")
        match polarity:
            case -1:
                self.send_command(self.oscilloscope, ":TRIG:EDGE:SLOP POS")
            case 1:
                self.send_command(self.oscilloscope, ":TRIG:EDGE:SLOP NEG")

        # setting type sweep
        self.send_command(self.oscilloscope, ":TRIG:SWE SING")

        self.send_command(self.oscilloscope, f":TIM:SCAL {tim_scale}")
        self.send_command(self.oscilloscope, f":TIM:POS {tim_scale*2}")

        for ch in channels:
            self.send_command(self.oscilloscope, f":CHAN{ch.index}:SCAL {ch.scale}")

        self.detect_errors(self.oscilloscope)

    def v2_move_oscilloscope_Y_axis(self, channels:list[Channel]):
        self.v2_oscilloscope_ping()
        match len(channels):
            case 1:
                pass
            case 2:
                self.send_command(self.oscilloscope, f":CHAN{channels[0].index}:OFFS {channels[0].scale*2}")
                self.send_command(self.oscilloscope, f":CHAN{channels[1].index}:OFFS {channels[1].scale*(-2)}")
            case 3:
                self.send_command(self.oscilloscope, f":CHAN{channels[0].index}:OFFS {channels[0].scale*2}")
                self.send_command(self.oscilloscope, f":CHAN{channels[1].index}:OFFS {channels[1].scale*(-2)}")
            case 4:
                self.send_command(self.oscilloscope, f":CHAN{channels[0].index}:OFFS {channels[0].scale}")
                self.send_command(self.oscilloscope, f":CHAN{channels[1].index}:OFFS {channels[1].scale*(-1)}")
                self.send_command(self.oscilloscope, f":CHAN{channels[2].index}:OFFS {channels[2].scale*3}")
                self.send_command(self.oscilloscope, f":CHAN{channels[3].index}:OFFS {channels[3].scale*(-3)}")
        self.detect_errors(self.oscilloscope)

    def v2_get_oscilloscope_data(self):
        self.v2_oscilloscope_ping()
        count = 0
        while True:
            self.send_command(self.oscilloscope, f":WAVeform:SOURce CHAN1")
            if self.query(self.oscilloscope, ":WAV:COMP?") == "100":
                break
            self.send_command(self.oscilloscope, f":WAVeform:SOURce CHAN2")
            if self.query(self.oscilloscope, ":WAV:COMP?") == "100":
                break
            self.send_command(self.oscilloscope, f":WAVeform:SOURce CHAN3")
            if self.query(self.oscilloscope, ":WAV:COMP?") == "100":
                break
            self.send_command(self.oscilloscope, f":WAVeform:SOURce CHAN4")
            if self.query(self.oscilloscope, ":WAV:COMP?") == "100":
                break

            count += 1
            if count == 5000:
                print("No waveforms data.")
                #raise Exception("No waveforms data.")
        
        data = {}
        for i in range(1, 5):
            match self.query(self.oscilloscope, f":CHAN{i}?"):
                case "OFF" | "0":
                    data[i] = []
                case "ON" | "1":
                    data[i] = [float(elem) for elem in self.query(self.oscilloscope, f":WAVeform:SOURce CHAN{i};DATA?").split(",")[:-1]]
        self.detect_errors(self.oscilloscope)
        return data
    
    def v2_get_sample(self) -> OscilloscopeData:
        self.v2_oscilloscope_ping()
        sample = OscilloscopeData(
            self.v2_get_oscilloscope_data(),
            float(self.query(self.oscilloscope, ":WAV:XOR?")),
            float(self.query(self.oscilloscope, ":WAV:XINC?")),
        )
        self.detect_errors(self.oscilloscope)
        return sample

    def v2_oscilloscope_run(self):
        self.v2_oscilloscope_ping()
        self.send_command(self.oscilloscope, ":RUN")
        self.detect_errors(self.oscilloscope)

    def v2_measure_oscilloscope(self):
        self.v2_oscilloscope_ping()
        """
        too many manipulation to do this
        need to return measures from oscilloscope

        Use this function after get data.

        Template:
        config.osc
        for t in tests:
            config.gen
            
        """
        self.detect_errors(self.oscilloscope)
        pass

    def v2_generator_ping(self):
        try:
            self.query(self.generator, COMMAND_IDN)
        except:
            raise Exception("No generator connection.")

    def v2_oscilloscope_ping(self):
        try:
            self.query(self.oscilloscope, COMMAND_IDN)
        except:
            raise Exception("No oscilloscope connection.")
        
    def v2_take_screen(self) -> list[bytes]:
        size = 8
        self.send_command(self.oscilloscope, ":DISPlay:DATA? PNG")
        bts = b''
        while True:
            try:
                bts += self.oscilloscope.read_bytes(size)
            except:
                return bts[7:]
