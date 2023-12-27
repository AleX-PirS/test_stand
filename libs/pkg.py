import json
import os
import glob
import matplotlib.pyplot  as plt
import numpy as np

scenarios_path = os.path.dirname(os.path.abspath(__file__)) + r'\scenarios\\'

registers_metadata_name_to_addr = {
    # ADC read regs
    'adc_val_0': 0,
    'adc_val_1': 1,
    'adc_val_2': 2,
    'adc_val_3': 3,
    'adc_val_4': 4,
    'adc_val_lsb_0': 5,
    'adc_val_lsb_1': 6,
    'adc_0_num': 8,
    'adc_1_num': 9,
    'adc_2_num': 10,
    'adc_3_num': 11,
    'adc_4_num': 12,
    # Last data read regs
    'last_data_0': 16,
    'last_data_1': 17,
    'last_data_2': 18,
    'last_data_3': 19,
    'last_data_4': 20,
    'last_data_5': 21,
    'last_data_6': 22,
    'last_data_7': 23,
    'last_data_8': 24,
    'last_data_9': 25,
    'last_data_10': 26,
    'last_data_11': 27,
    # PF_and_CMP read regs
    'pf_and_cmp_0': 32,
    'pf_and_cmp_1': 33,
    'pf_and_cmp_2': 34,
    'pf_and_cmp_3': 35,
    'pf_and_cmp_4': 36,
    'pf_and_cmp_5': 37,
    'pf_and_cmp_6': 38,
    'pf_and_cmp_7': 39,
    'pf_and_cmp_8': 40,
    'pf_and_cmp_9': 41,
    'pf_and_cmp_10': 42,
    'pf_and_cmp_11': 43,
    'pf_and_cmp_12': 44,
    'pf_and_cmp_13': 45,
    'pf_and_cmp_14': 46,
    'pf_and_cmp_15': 47,
    'pf_and_cmp_16': 48,

    # Analog regs
    'analog_ctrl_0': 65,
    'analog_ctrl_1': 66,
    'dac_cal': 67,
    'cal_en_0': 68,
    'cal_en_1': 69,
    'rez': 70,
    # 'an_ch_disable_0' : 96,
    # 'an_ch_disable_1' : 97,
    # 'an_ch_disable_2' : 98,
    # 'an_ch_disable_3' : 99,
    # 'an_ch_disable_4' : 100,
    # 'an_ch_disable_5' : 101,
    # 'an_ch_disable_6' : 102,
    # 'an_ch_disable_7' : 103,
    # 'an_ch_disable_8' : 104,
    # 'an_ch_disable_9' : 105,
    # 'an_ch_disable_10' : 106,
    # 'an_ch_disable_11' : 107,
    # 'an_ch_disable_12' : 108,
    # 'an_ch_disable_13' : 109,
    # 'an_ch_disable_14' : 110,
    'an_ch_disable_15': 111,
    'an_ch_disable_16': 112,
    # Analog-digital regs
    'digit_analog_ctrl_0': 72,
    # Digital regs
    'cfg_p1_in_time': 80,
    'cfg_p1_l0_over': 81,
    'cfg_p2_plus_soc': 82,
    'cfg_p2_plus_swm': 83,
    'cfg_p2_plus_eoc': 84,
    'cfg_rst_plus_eoc': 85,
    'cfg_p3_l1_over_0': 86,
    'cfg_p3_l1_over_1': 87,
    'cfg_out_int': 88,
    'cfg_clk_gen_0': 90,
    'cfg_clk_gen_1': 91,
    'cfg_sw_force_num': 92,
    'cfg_sw_force_en': 93,
    # 'cfg_ch_emul_0' : 120,
    # 'cfg_ch_emul_1' : 121,
    'cfg_ch_emul_2': 122,
    'cfg_ch_emul_3': 123,
    'cfg_ch_emul_4': 124,
}

r_regs_start_addr_count = (
    (0, 7),
    (8, 5),
    (16, 12),
    (32, 17),
)

rw_regs_start_addr_count = (
    (65, 6),
    (72, 2), # Поменял на длину 2, но вдруг что то задену
    # (72, 1), было так, но почему то юарт на обрабатывает длину 1
    (80, 9),
    (90, 4),
    (111, 2),
    (122, 3),
)

registers_metadata_addr_to_name = {
        # ADC read regs
        0: 'adc_val_0',
        1: 'adc_val_1',
        2: 'adc_val_2',
        3: 'adc_val_3',
        4: 'adc_val_4',
        5: 'adc_val_lsb_0',
        6: 'adc_val_lsb_1',
        8: 'adc_0_num',
        9: 'adc_1_num',
        10: 'adc_2_num',
        11: 'adc_3_num',
        12: 'adc_4_num',
        # Last data read regs
        16: 'last_data_0',
        17: 'last_data_1',
        18: 'last_data_2',
        19: 'last_data_3',
        20: 'last_data_4',
        21: 'last_data_5',
        22: 'last_data_6',
        23: 'last_data_7',
        24: 'last_data_8',
        25: 'last_data_9',
        26: 'last_data_10',
        27: 'last_data_11',
        # PF_and_CMP read regs
        32: 'pf_and_cmp_0',
        33: 'pf_and_cmp_1',
        34: 'pf_and_cmp_2',
        35: 'pf_and_cmp_3',
        36: 'pf_and_cmp_4',
        37: 'pf_and_cmp_5',
        38: 'pf_and_cmp_6',
        39: 'pf_and_cmp_7',
        40: 'pf_and_cmp_8',
        41: 'pf_and_cmp_9',
        42: 'pf_and_cmp_10',
        43: 'pf_and_cmp_11',
        44: 'pf_and_cmp_12',
        45: 'pf_and_cmp_13',
        46: 'pf_and_cmp_14',
        47: 'pf_and_cmp_15',
        48: 'pf_and_cmp_16',

        # Analog regs
        65: 'analog_ctrl_0',
        66: 'analog_ctrl_1',
        67: 'dac_cal',
        68: 'cal_en_0',
        69: 'cal_en_1',
        70: 'rez',
        # 96 : 'an_ch_disable_0',
        # 97 : 'an_ch_disable_1',
        # 98 : 'an_ch_disable_2',
        # 99 : 'an_ch_disable_3',
        # 100 : 'an_ch_disable_4',
        # 101 : 'an_ch_disable_5',
        # 102 : 'an_ch_disable_6',
        # 103 : 'an_ch_disable_7',
        # 104 : 'an_ch_disable_8',
        # 105 : 'an_ch_disable_9',
        # 106 : 'an_ch_disable_10',
        # 107 : 'an_ch_disable_11',
        # 108 : 'an_ch_disable_12',
        # 109 : 'an_ch_disable_13',
        # 110 : 'an_ch_disable_14',
        111: 'an_ch_disable_15',
        112: 'an_ch_disable_16',
        # Analog-digital regs
        72: 'digit_analog_ctrl_0',
        # Digital regs
        80: 'cfg_p1_in_time',
        81: 'cfg_p1_l0_over',
        82: 'cfg_p2_plus_soc',
        83: 'cfg_p2_plus_swm',
        84: 'cfg_p2_plus_eoc',
        85: 'cfg_rst_plus_eoc',
        86: 'cfg_p3_l1_over_0',
        87: 'cfg_p3_l1_over_1',
        88: 'cfg_out_int',
        90: 'cfg_clk_gen_0',
        91: 'cfg_clk_gen_1',
        92: 'cfg_sw_force_num',
        93: 'cfg_sw_force_en',
        # 120 : 'cfg_ch_emul_0',
        # 121 : 'cfg_ch_emul_1',
        122: 'cfg_ch_emul_2',
        123: 'cfg_ch_emul_3',
        124: 'cfg_ch_emul_4',
    }


class RegData(object):
    reg_data = [int.to_bytes(0, 1, 'big') for _ in range(125)]

    DEFAULT_CCAL=0b01
    DEFAULT_CCSA=0b01
    DEFAULT_GAIN=0b0
    DEFAULT_ICSA=0b0
    DEFAULT_SHA=0b11
    DEFAULT_SHTR=0b00
    DEFAULT_POL=0b1
    DEFAULT_BIAS_CORE_CUR=0b00
    DEFAULT_DAC_CAL=0b0000_0000
    DEFAULT_REZ=0b0000_0000
    DEFAULT_CAL_EN_CH=0b0000_0000_00
    DEFAULT_AN_CH_DISABLE=0b0000_0000_00
    DEFAULT_CMP_TH=0b0001
    DEFAULT_CFG_p1_in_time=0b01011
    DEFAULT_CFG_p1_L0_over=0b10101
    DEFAULT_CFG_p2_plus_SOC=0b01000
    DEFAULT_CFG_p2_plus_SWM=0b01010
    DEFAULT_CFG_p2_plus_EOC=0b00100
    DEFAULT_CFG_p3_L1_over=0b0110_0100_01
    DEFAULT_CFG_rst_plus_EOC=0b01000
    DEFAULT_CFG_SW_force_num=0b0000_0000
    DEFAULT_CFG_SW_force_EN=0b0
    DEFAULT_CFG_OUT_INT=0b0000_000
    DEFAULT_ADC_EMU_CFG=0b0000_0000_00
    DEFAULT_EMUL_DATA_i=0b0000_0
    DEFAULT_EMUL_ADDR_i=0b000
    DEFAULT_EMUL_EN_L0=0b0
    DEFAULT_EMUL_EN_L1=0b0
    DEFAULT_EMUL_tau_v=0b00
    DEFAULT_EMUL_L0_v=0b00
    DEFAULT_EMUL_L1_v=0b0000_0000

    def __init__(self,
                 is_zero_init=False,
                 template_list = [],
                 # Analog
                 CCAL=DEFAULT_CCAL,
                 CCSA=DEFAULT_CCSA,
                 GAIN=DEFAULT_GAIN,
                 ICSA=DEFAULT_ICSA,
                 SHA=DEFAULT_SHA,
                 SHTR=DEFAULT_SHTR,
                 POL=DEFAULT_POL,
                 BIAS_CORE_CUR=DEFAULT_BIAS_CORE_CUR,
                 DAC_CAL=DEFAULT_DAC_CAL,
                 REZ=DEFAULT_REZ,
                 CAL_EN_CH=DEFAULT_CAL_EN_CH,
                 AN_CH_DISABLE=DEFAULT_AN_CH_DISABLE,
                 # Analog-digital
                 CMP_TH=DEFAULT_CMP_TH,
                 # Digital
                 CFG_p1_in_time=DEFAULT_CFG_p1_in_time,
                 CFG_p1_L0_over=DEFAULT_CFG_p1_L0_over,
                 CFG_p2_plus_SOC=DEFAULT_CFG_p2_plus_SOC,
                 CFG_p2_plus_SWM=DEFAULT_CFG_p2_plus_SWM,
                 CFG_p2_plus_EOC=DEFAULT_CFG_p2_plus_EOC,
                 CFG_p3_L1_over=DEFAULT_CFG_p3_L1_over,
                 CFG_rst_plus_EOC=DEFAULT_CFG_rst_plus_EOC,
                 CFG_SW_force_num=DEFAULT_CFG_SW_force_num,
                 CFG_SW_force_EN=DEFAULT_CFG_SW_force_EN,
                 CFG_OUT_INT=DEFAULT_CFG_OUT_INT,
                 ADC_EMU_CFG=DEFAULT_ADC_EMU_CFG,
                 EMUL_DATA_i=DEFAULT_EMUL_DATA_i,
                 EMUL_ADDR_i=DEFAULT_EMUL_ADDR_i,
                 EMUL_EN_L0=DEFAULT_EMUL_EN_L0,
                 EMUL_EN_L1=DEFAULT_EMUL_EN_L1,
                 EMUL_tau_v=DEFAULT_EMUL_tau_v,
                 EMUL_L0_v=DEFAULT_EMUL_L0_v,
                 EMUL_L1_v=DEFAULT_EMUL_L1_v,
                 ) -> None:

        if is_zero_init:
            self.reg_data = [-1 for _ in range(125)]
            return
        
        if len(template_list) != 0:
            self.reg_data = [int.to_bytes(int_byte, 1, 'big') for int_byte in template_list]
            return

        self.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']] = int.to_bytes(
            (CCAL << 6)+(CCSA << 4)+(GAIN << 3)+(ICSA << 2)+(SHA), 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['analog_ctrl_1']] = int.to_bytes(
            (SHTR << 6)+(POL << 5)+(BIAS_CORE_CUR << 3), 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['dac_cal']] = int.to_bytes(
            DAC_CAL, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cal_en_0']] = int.to_bytes(
            CAL_EN_CH >> 2, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cal_en_1']] = int.to_bytes(
            (0b11 & CAL_EN_CH) << 6, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['rez']
                      ] = int.to_bytes(REZ, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['an_ch_disable_15']] = int.to_bytes(
            AN_CH_DISABLE >> 2, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['an_ch_disable_16']] = int.to_bytes(
            (0b11 & AN_CH_DISABLE) << 6, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['digit_analog_ctrl_0']] = int.to_bytes(
            CMP_TH, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p1_in_time']] = int.to_bytes(
            CFG_p1_in_time, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p1_l0_over']] = int.to_bytes(
            CFG_p1_L0_over, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_soc']] = int.to_bytes(
            CFG_p2_plus_SOC, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_swm']] = int.to_bytes(
            CFG_p2_plus_SWM, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_eoc']] = int.to_bytes(
            CFG_p2_plus_EOC, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_rst_plus_eoc']] = int.to_bytes(
            CFG_rst_plus_EOC, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p3_l1_over_0']] = int.to_bytes(
            CFG_p3_L1_over >> 5, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_p3_l1_over_1']] = int.to_bytes(
            0b11111 & CFG_p3_L1_over, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_out_int']] = int.to_bytes(
            CFG_OUT_INT, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_clk_gen_0']] = int.to_bytes(
            ADC_EMU_CFG >> 2, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_clk_gen_1']] = int.to_bytes(
            (0b11 & ADC_EMU_CFG) << 6, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_sw_force_num']] = int.to_bytes(
            CFG_SW_force_num, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_sw_force_en']] = int.to_bytes(
            CFG_SW_force_EN, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_2']] = int.to_bytes(
            EMUL_L1_v, 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_3']] = int.to_bytes(
            (EMUL_L0_v << 4)+(EMUL_tau_v << 2)+(EMUL_EN_L1 << 1)+(EMUL_EN_L0), 1, 'big')
        self.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_4']] = int.to_bytes(
            (EMUL_ADDR_i << 5)+(EMUL_DATA_i), 1, 'big')
        return

    def __str__(self) -> str:
        res = ""
        for i in range(len(self.reg_data)):
            if i not in registers_metadata_addr_to_name:
                continue
            if self.reg_data[i] == -1:
                continue
            res += f'Addr:{i}, "{registers_metadata_addr_to_name[i]}":"{int.from_bytes(self.reg_data[i], "big"):08b}"\n'

        return res[:-1]
    
    def toJSON(self):
        reg_data_int = [int.from_bytes(i, 'big') for i in self.reg_data]
        return json.dumps(reg_data_int, default=lambda o: o.__dict__, sort_keys=True, indent=4)      


class GeneratorSample(object):
    def __init__(self, signal_type, offset, delay, width, lead, trail, ampl, freq, is_triggered, trig_lvl) -> None:
        self.signal_type = signal_type
        self.offset = offset
        self.delay = delay
        self.width = width
        self.lead = lead
        self.trail = trail
        self.ampl = ampl
        self.freq = freq
        self.is_triggered = is_triggered
        self.trig_lvl = trig_lvl

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Channel(object):
    def __init__(self, name:str, index:int, scale:int) -> None:
        self.name = name
        self.index = index
        self.scale = scale


class OscilloscopeData(object):
    def __init__(self, data, origin, delta) -> None:
        self.data = {1:[[],[]], 2:[[],[]], 3:[[],[]], 4:[[],[]]}
        for i in range(1, 5):
            self.data[i][0] = [origin+i*delta for i in range(len(data[i]))]
            self.data[i][1] = data[i]

    def __str__(self) -> str:
        res = ""
        for i in range(1, 5):
            if len(self.data[i][0]) == 0:
                continue
            res += f"Channel{i}:\n"
            res += f"X Axis:\n"
            for data in self.data[i][0]:
                res += f"{data} "

            res += f"\nY Axis:\n"
            for data in self.data[i][1]:
                res += f"{data} "

        return res
    
    # def plot_one(self, index, label):
    #     _, ax = plt.subplots(2,2)
    #     ax.plot(self.data[index][0], self.data[index][1], linewidth=1.0)
    #     plt.show()

    def plot_all(self, channels:list[Channel]):
        # match len(channels):
        #     case 1:
        #         fig, axs = plt.subplots(1, 1)
        #     case 2:
        #         fig, axs = plt.subplots(2, 1)
        #     case 3:
        #         fig, axs = plt.subplots(2, 2)
        #     case 4:
        #         fig, axs = plt.subplots(2, 2)


        
        fig, axs = plt.subplots(2, 2)
        for ch in channels:
            match ch.index:
                case 1:
                    axs[0, 0].plot(self.data[1][0], self.data[1][1])
                    axs[0, 0].set_title(ch.name)
                    axs[0, 0].set_xlabel("s")
                    axs[0, 0].set_ylabel("")
                    axs[0, 0].grid(True, which='both')
                case 2:
                    axs[0, 1].plot(self.data[2][0], self.data[2][1])
                    axs[0, 1].set_title(ch.name)
                    axs[0, 1].set_xlabel("s")
                    axs[0, 1].set_ylabel("V")
                    axs[0, 1].grid(True, which='both')
                case 3:
                    axs[1, 0].plot(self.data[3][0], self.data[3][1])
                    axs[1, 0].set_title(ch.name)
                    axs[1, 0].set_xlabel("s")
                    axs[1, 0].set_ylabel("V")
                    axs[1, 0].grid(True, which='both')
                case 4:
                    axs[1, 1].plot(self.data[4][0], self.data[4][1])
                    axs[1, 1].set_title(ch.name)
                    axs[1, 1].set_xlabel("s")
                    axs[1, 1].set_ylabel("V")
                    axs[1, 1].grid(True, which='both')

        plt.show()


class TestSample(object):
    def __init__(self, constants:RegData, samples:list[GeneratorSample]) -> None:
        self.test_count = len(samples)
        self.constants = [int.from_bytes(i, 'big') for i in constants.reg_data]
        self.samples = samples

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    
class Scenario(object):
    def __init__(self, channels:list[Channel] = [], name:str='default name', description:str="", tests:list[TestSample] = [], trig_src=0, trig_lvl=0, tim_scale=0) -> None:
        self.channels = channels
        self.trig_src = trig_src
        self.trig_lvl = trig_lvl
        self.tim_scale = tim_scale
        self.name = name
        self.description = description
        self.total_test_count = 0
        self.layers_count = len(tests)
        for i in tests:
            self.total_test_count += i.test_count
        self.tests = tests

    def add_layer(self, test:TestSample):
        self.layers_count += 1
        self.tests.append(test)
        self.total_test_count += test.test_count

    def delete_last_layer(self):
        if self.layers_count == 0:
            return
        self.layers_count -= 1
        test = self.tests[-1]
        self.tests = self.tests[:-1]
        self.total_test_count -= test.test_count

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def fromJSON(self, file):
        data = json.load(file)
        channels = []
        for ch in data['channels']:
            chan = Channel(
                name=ch['name'],
                index=ch['index'],
                scale=ch['scale'],
            )
            channels.append(chan)
            
        self.channels = channels
        self.trig_src = data['trig_src']
        self.trig_lvl = data['trig_lvl']
        self.tim_scale = data['tim_scale']
        self.description = data['description']
        self.layers_count = data['layers_count']
        self.name = data['name']
        self.total_test_count = data['total_test_count']

        for test in data['tests']:
            test_reg_bytes = RegData()
            test_reg_bytes.reg_data = [int.to_bytes(i, 1, 'big') for i in test['constants']]
            tests = TestSample(test_reg_bytes, [])
            tests.test_count = test['test_count']

            for sample in test['samples']:
                smpl = GeneratorSample(
                    ampl=sample['ampl'],
                    delay=sample['delay'],
                    freq=sample['freq'],
                    is_triggered=sample['is_triggered'],
                    lead=sample['lead'],
                    offset=sample['offset'],
                    signal_type=sample['signal_type'],
                    trail=sample['trail'],
                    width=sample['width'],
                    trig_lvl=sample['trig_lvl'],
                )
                tests.samples.append(smpl)
            self.tests.append(tests)

    def save_scenario(self)->None:
        with open(scenarios_path + self.name+'.json', 'w') as file:
            data = self.toJSON()
            file.write(data)
            file.close

def find_scenarios()-> list[Scenario]:
    scenarios = []
    for file in glob.glob(scenarios_path+"*.json"):
        with open(file) as f:
            data = Scenario([], "", "", [], 0, 0, 0)
            try:
                data.fromJSON(f)
            except:
                continue
            scenarios.append(data)
            f.close()
    return scenarios

def process_signal_type(signal) -> str:
    match signal:
        case "Pulse":
            return "PULS"
        case "Square":
            return "SQU"
        case "Sine":
            return "SIN"
        case "Ramp":
            return "RAMP"
        case "Noise":
            return "NOIS"
        case "Arb":
            return "USER"
        case _:
            raise Exception("Bad signal type.")
        