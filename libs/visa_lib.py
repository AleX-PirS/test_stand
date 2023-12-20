from numpy import mat
import pyvisa as visa

from pkg import Channel, GeneratorSample

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

    def connect_gen(self, address: str):
        self.generator = self.connect_resource(address, QUERY_GENERATOR)

    def clear_resource(self, resource):
        self.send_command(resource, COMMAND_CLEAR)
        self.send_command(resource, COMMAND_RESET)

    def reset_resource(self, resource: visa.Resource):
        self.clear_resource(resource)
        resource.close()

    def reset_oscilloscope(self):
        self.v2_oscilloscope_ping()
        self.reset_resource(self.oscilloscope)

    def reset_generator(self):
        self.v2_generator_ping()
        self.reset_resource(self.generator)

    def prep_oscilloscope(self, chan_numb: int, trig_lvl: int):
        self.send_command(
            self.oscilloscope, f":CHAN{str(chan_numb)}:PROB {CHANNEL_PROB_CONST}")
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

    # def configure_generator_sample(self, data: SampleSettings):
    #     signal_type = self.signal_type_from_box(data.get_signal_type())

    #     self.send_command(self.generator, f":FUNC {signal_type}")
    #     self.send_command(self.generator, f":FREQ {data.get_freq()}Hz")
    #     self.send_command(self.generator, f":VOLT:HIGH {data.get_ampl()}mV")
    #     self.send_command(self.generator, f":VOLT:LOW 0V")
    #     self.send_command(
    #         self.generator, f":FUNC:{signal_type}:WIDT {data.get_width()}ns")
    #     self.send_command(
    #         self.generator, f":FUNC:{signal_type}:DEL {data.get_delay()}s")
    #     self.send_command(
    #         self.generator, f":FUNC:{signal_type}:TRAN {data.get_lead()}ns")
    #     self.send_command(
    #         self.generator, f":FUNC:{signal_type}:TRAN:TRA {data.get_trail()}ns")

    #     errors = self.detect_errors(self.generator)

    #     if errors != "":
    #         raise Exception("invalid signal settings", errors)

    # def measure(self, chan_num: int) -> Sample:
    #     Edge = self.query(self.oscilloscope,
    #                       f":MEAS:EDGE? CHAN{str(chan_num)}")
    #     Amplitude = self.query(
    #         self.oscilloscope, f":MEAS:VAMP? CHAN{str(chan_num)}")
    #     Fall = self.query(self.oscilloscope,
    #                       f":MEAS:FALL? CHAN{str(chan_num)}")
    #     Frequency = self.query(
    #         self.oscilloscope, f":MEAS:FREQ? CHAN{str(chan_num)}")

    #     sample = Sample(edge=Edge, ampl=Amplitude, fall=Fall, freq=Frequency)

    #     return sample

    # def do_sample(self, chan_num: int, generator_settings: SampleSettings, trig_lvl: int):
    #     self.send_command(self.generator, f":OUTP{str(chan_num)} ON")
    #     try:
    #         self.configure_generator_sample(generator_settings)
    #     except Exception as e:
    #         if e.args[0] == self.EXCEPTION_INVALID_SIGNAL_SETTINGS:
    #             print("Bad signal settings")
    #             return e.args[1]
    #         return

    #     self.prep_oscilloscope(chan_num, trig_lvl)
    #     self.send_command(self.oscilloscope, ":SING")
    #     self.send_command(self.oscilloscope, f":MEAS:SOUR CHAN{str(chan_num)}")

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
    
    def v2_configurate_generator_sample(self, config:GeneratorSample):
        self.v2_generator_ping()
        self.clear_resource(self.generator)
        self.send_command(self.generator, f":FUNC {config.signal_type}")
        self.send_command(self.generator, f":FREQ {config.freq}kHz")
        # self.send_command(self.generator, f":VOLT:HIGH {config.offset}mV")
        if config.is_triggered:
            self.send_command(self.generator, f":ARM:SOUR EXT")
            self.send_command(self.generator, f":ARM:LEV {config.trig_lvl}mV")
        else:
            self.send_command(self.generator, f":ARM:SOUR IMM")

        match config.signal_type:
            case "PULS":
                self.send_command(self.generator, f":FUNC:{config.signal_type}:WIDT {config.width}ns")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:TRAN {config.lead}ns")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:TRAN:TRA {config.trail}ns")
                self.send_command(self.generator, f":FUNC:{config.signal_type}:DEL {config.delay}ns")
                self.send_command(self.generator, f":VOLT:HIGH {float(config.ampl)+float(config.offset)}mV")
                self.send_command(self.generator, f":VOLT:LOW {float(config.offset)}mV")
            case "SQU" | "RAMP" | "SIN" | "USER":
                self.send_command(self.generator, f":VOLT:OFFS {config.offset}mV")
                self.send_command(self.generator, f":VOLT {config.ampl}mV")
                pass
            case "NOIS":
                self.send_command(self.generator, f":VOLT:OFFS {config.offset}mV")
                self.send_command(self.generator, f":VOLT {config.ampl}mV")
                pass

        self.detect_errors(self.generator)
    
    def v2_toggle_out1(self):
        self.v2_generator_ping()
        # Добавить все тоже самое для не out
        match self.query(self.generator, f":OUTP1?"):
            case "OFF" | "0":
                self.send_command(self.generator, ":OUTP1 ON")
            case "ON" | "1":
                self.send_command(self.generator, ":OUTP1 OFF")
        self.detect_errors(self.generator)

    def v2_on_out1(self):
        self.v2_generator_ping()
        self.send_command(self.generator, f":OUTP1 ON")
        self.detect_errors(self.generator)
    
    def v2_off_out1(self):
        self.v2_generator_ping()
        self.send_command(self.generator, f":OUTP1 OFF")
        self.detect_errors(self.generator)

    def v2_configurate_oscilloscope_sample(self, channels:list[Channel], trig_src, trig_lvl):
        self.v2_oscilloscope_ping()
        self.clear_resource(self.oscilloscope)
        for i in range(1, 5):
            self.send_command(self.oscilloscope, f":CHAN{i} OFF")
        for ch in channels:
            self.send_command(self.oscilloscope, f":CHAN{ch.index} ON")
        # trigger settings
        self.send_command(self.oscilloscope, ":TRIG:MODE EDGE")
        self.send_command(self.oscilloscope, f":TRIG:EDGE:SOUR CHAN{trig_src}")
        self.send_command(self.oscilloscope, f":TRIG:LEV CHAN{trig_src}, {trig_lvl}mV")
        self.send_command(self.oscilloscope, ":TRIG:EDGE:SLOP POS")
        # setting type sweep
        self.send_command(self.oscilloscope, ":TRIG:SWE SING")
        self.detect_errors(self.oscilloscope)

    def v2_set_oscilloscope_Y_scale(self, config:GeneratorSample):
        self.v2_oscilloscope_ping()
        
        self.detect_errors(self.oscilloscope)

    def v2_set_oscilloscope_X_scale(self, config:GeneratorSample):
        self.v2_oscilloscope_ping()
        
        self.detect_errors(self.oscilloscope)

    def v2_move_oscilloscope_Y_axis(self, config:GeneratorSample):
        self.v2_oscilloscope_ping()
        
        self.detect_errors(self.oscilloscope)

    def v2_move_oscilloscope_X_axis(self, config:GeneratorSample):
        self.v2_oscilloscope_ping()
        
        self.detect_errors(self.oscilloscope)

        """
        # :ACQuire:AVERage ON
        # :ACQuire:COUNt 64
        # :ACQuire:BANDwidth MAX
        # :ACQuire:COMPlete 100
        # :ACQuire:MODE RTIMe
        # :ACQuire:POINts:AUTO ON
        # Как будто они и не нужны для тестов

        :WAVeform:STReaming ON ?????
        :WAVeform:SOURce CHAN1;DATA?
        :WAVeform:COMPlete?

        Время: X-axis Units = data index x Xincrement + Xorigin
        :WAVeform:XORigin? старт отсчета точек по времени
        :WAVeform:XINCrement? шаг по времени

        :WAVeform:POINts? количество точек.

        :TIM:SCAL <время одного квадрата>
        :TIMebase:RANGe <время всего таймлайна>
        :TIMebase:WINDow:POSition <позиция по времени для сигналов>

        :CHAN<index>:SCAL <масштаб по сигналу>
        :CHANnel<N>:RANGe
        :CHAN3:OFFS <позиция>

        :RUN   когда режим сингл, то всегда будет при run его сохранение

        Y-axis Units = data value x Yincrement + Yorigin (analog channels) , where the data index starts at zero: 0, 1, 2,
        ..., n-1.
        """

    def v2_measure_oscilloscope(self):
        self.v2_oscilloscope_ping()
        """
        too many manipulation to do this
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
            self.query(self.generator, COMMAND_IDN)
        except:
            raise Exception("No oscilloscope connection.")
