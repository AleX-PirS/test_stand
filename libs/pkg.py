

class RegData(object):
    reg_data = [int.to_bytes(0, 1, 'big') for _ in range(125)]   

    def __init__(self,
                 # Analog
                 CCAL = 0b01,
                 CCSA = 0b01,
                 GAIN = 0b0,
                 ICSA = 0b0,
                 SHA = 0b11,
                 SHTR = 0b00,
                 POL = 0b1,
                 BIAS_CORE_CUR = 0b00,
                 DAC_CAL = 0b0000_0000,
                 REZ = 0b0000_0000,
                 CAL_EN_CH = 0b0000_0000_00,
                 AN_CH_DISABLE = 0b0000_0000_00,
                 # Analog-digital
                 CMP_TH = 0b0001,
                 # Digital
                 CFG_p1_in_time = 0b01011,
                 CFG_p1_L0_over = 0b10101,
                 CFG_p2_plus_SOC = 0b01000,
                 CFG_p2_plus_SWM = 0b01010,
                 CFG_p2_plus_EOC = 0b00100,
                 CFG_p3_L1_over = 0b0110_0100_01,
                 CFG_rst_plus_EOC = 0b01000,
                 CFG_SW_force_num = 0b0000_0000,
                 CFG_SW_force_EN = 0b0,
                 CFG_OUT_INT = 0b0000_000,
                 ADC_EMU_CFG = 0b0000_0000_00,
                 EMUL_DATA_i = 0b0000_0,
                 EMUL_ADDR_i = 0b000,
                 EMUL_EN_L0 = 0b0,
                 EMUL_EN_L1 = 0b0,
                 EMUL_tau_v = 0b00,
                 EMUL_L0_v = 0b00,
                 EMUL_L1_v = 0b0000_0000,
                 ) -> None:
        self.registers_metadata_addr_to_name = {
            # ADC read regs
            0 : 'adc_val_0',
            1 : 'adc_val_1',
            2 : 'adc_val_2',
            3 : 'adc_val_3',
            4 : 'adc_val_4',
            5 : 'adc_val_lsb_0',
            6 : 'adc_val_lsb_1',
            8 : 'adc_0_num',
            9 : 'adc_1_num',
            10 : 'adc_2_num',
            11 : 'adc_3_num',
            12 : 'adc_4_num',
            # Last data read regs
            16 : 'last_data_0',
            17 : 'last_data_1',
            18 : 'last_data_2',
            19 : 'last_data_3',
            20 : 'last_data_4',
            21 : 'last_data_5',
            22 : 'last_data_6',
            23 : 'last_data_7',
            24 : 'last_data_8',
            25 : 'last_data_9',
            26 : 'last_data_10',
            27 : 'last_data_11',
            # PF_and_CMP read regs
            32 : 'pf_and_cmp_0',
            33 : 'pf_and_cmp_1',
            34 : 'pf_and_cmp_2',
            35 : 'pf_and_cmp_3',
            36 : 'pf_and_cmp_4',
            37 : 'pf_and_cmp_5',
            38 : 'pf_and_cmp_6',
            39 : 'pf_and_cmp_7',
            40 : 'pf_and_cmp_8',
            41 : 'pf_and_cmp_9',
            42 : 'pf_and_cmp_10',
            43 : 'pf_and_cmp_11',
            44 : 'pf_and_cmp_12',
            45 : 'pf_and_cmp_13',
            46 : 'pf_and_cmp_14',
            47 : 'pf_and_cmp_15',
            48 : 'pf_and_cmp_16',

            # Analog regs
            65 : 'analog_ctrl_0',
            66 : 'analog_ctrl_1',
            67 : 'dac_cal',
            68 : 'cal_en_0',
            69 : 'cal_en_1',
            70 : 'rez',
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
            111 : 'an_ch_disable_15',
            112 : 'an_ch_disable_16',
            # Analog-digital regs
            72 : 'digit_analog_ctrl_0',
            # Digital regs
            80 : 'cfg_p1_in_time',
            81 : 'cfg_p1_l0_over',
            82 : 'cfg_p2_plus_soc',
            83 : 'cfg_p2_plus_swm',
            84 : 'cfg_p2_plus_eoc',
            85 : 'cfg_rst_plus_eoc',
            86 : 'cfg_p3_l1_over_0',
            87 : 'cfg_p3_l1_over_1',
            88 : 'cfg_out_int',
            90 : 'cfg_clk_gen_0',
            91 : 'cfg_clk_gen_1',
            92 : 'cfg_sw_force_num',
            93 : 'cfg_sw_force_en',
            # 120 : 'cfg_ch_emul_0',
            # 121 : 'cfg_ch_emul_1',
            122 : 'cfg_ch_emul_2',
            123 : 'cfg_ch_emul_3',
            124 : 'cfg_ch_emul_4',
        }

        self.registers_metadata_name_to_addr = {
            # ADC read regs
            'adc_val_0' : 0,
            'adc_val_1' : 1,
            'adc_val_2' : 2,
            'adc_val_3' : 3,
            'adc_val_4' : 4,
            'adc_val_lsb_0' : 5,
            'adc_val_lsb_1' : 6,
            'adc_0_num' : 8,
            'adc_1_num' : 9,
            'adc_2_num' : 10,
            'adc_3_num' : 11,
            'adc_4_num' : 12,
            # Last data read regs
            'last_data_0' : 16,
            'last_data_1' : 17,
            'last_data_2' : 18,
            'last_data_3' : 19,
            'last_data_4' : 20,
            'last_data_5' : 21,
            'last_data_6' : 22,
            'last_data_7' : 23,
            'last_data_8' : 24,
            'last_data_9' : 25,
            'last_data_10' : 26,
            'last_data_11' : 27,
            # PF_and_CMP read regs
            'pf_and_cmp_0' : 32,
            'pf_and_cmp_1' : 33,
            'pf_and_cmp_2' : 34,
            'pf_and_cmp_3' : 35,
            'pf_and_cmp_4' : 36,
            'pf_and_cmp_5' : 37,
            'pf_and_cmp_6' : 38,
            'pf_and_cmp_7' : 39,
            'pf_and_cmp_8' : 40,
            'pf_and_cmp_9' : 41,
            'pf_and_cmp_10' : 42,
            'pf_and_cmp_11' : 43,
            'pf_and_cmp_12' : 44,
            'pf_and_cmp_13' : 45,
            'pf_and_cmp_14' : 46,
            'pf_and_cmp_15' : 47,
            'pf_and_cmp_16' : 48,

            # Analog regs
            'analog_ctrl_0' : 65,
            'analog_ctrl_1' : 66,
            'dac_cal' : 67,
            'cal_en_0' : 68,
            'cal_en_1' : 69,
            'rez' : 70,
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
            'an_ch_disable_15' : 111,
            'an_ch_disable_16' : 112,
            # Analog-digital regs
            'digit_analog_ctrl_0' : 72,
            # Digital regs
            'cfg_p1_in_time' : 80,
            'cfg_p1_l0_over' : 81,
            'cfg_p2_plus_soc' : 82,
            'cfg_p2_plus_swm' : 83,
            'cfg_p2_plus_eoc' : 84,
            'cfg_rst_plus_eoc' : 85,
            'cfg_p3_l1_over_0' : 86,
            'cfg_p3_l1_over_1' : 87,
            'cfg_out_int' : 88,
            'cfg_clk_gen_0' : 90,
            'cfg_clk_gen_1' : 91,
            'cfg_sw_force_num' : 92,
            'cfg_sw_force_en' : 93,
            # 'cfg_ch_emul_0' : 120,
            # 'cfg_ch_emul_1' : 121,
            'cfg_ch_emul_2' : 122,
            'cfg_ch_emul_3' : 123,
            'cfg_ch_emul_4' : 124,
        }

        self.reg_data[self.registers_metadata_name_to_addr['analog_ctrl_0']] = int.to_bytes((CCAL<<6)+(CCSA<<4)+(GAIN<<3)+(ICSA<<2)+(SHA), 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['analog_ctrl_1']] = int.to_bytes((SHTR<<6)+(POL<<5)+(BIAS_CORE_CUR<<3), 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['dac_cal']] = int.to_bytes(DAC_CAL, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cal_en_0']] = int.to_bytes(CAL_EN_CH>>2, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cal_en_1']] = int.to_bytes((0b11&CAL_EN_CH)<<6, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['rez']] = int.to_bytes(REZ, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['an_ch_disable_15']] = int.to_bytes(AN_CH_DISABLE>>2, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['an_ch_disable_16']] = int.to_bytes((0b11&AN_CH_DISABLE)<<6, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['digit_analog_ctrl_0']] = int.to_bytes(CMP_TH, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p1_in_time']] = int.to_bytes(CFG_p1_in_time, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p1_l0_over']] = int.to_bytes(CFG_p1_L0_over, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p2_plus_soc']] = int.to_bytes(CFG_p2_plus_SOC, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p2_plus_swm']] = int.to_bytes(CFG_p2_plus_SWM, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p2_plus_eoc']] = int.to_bytes(CFG_p2_plus_EOC, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_rst_plus_eoc']] = int.to_bytes(CFG_rst_plus_EOC, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p3_l1_over_0']] = int.to_bytes(CFG_p3_L1_over>>5, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_p3_l1_over_1']] = int.to_bytes(0b11111&CFG_p3_L1_over, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_out_int']] = int.to_bytes(CFG_OUT_INT, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_clk_gen_0']] = int.to_bytes(ADC_EMU_CFG>>2, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_clk_gen_1']] = int.to_bytes((0b11&ADC_EMU_CFG)<<6, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_sw_force_num']] = int.to_bytes(CFG_SW_force_num, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_sw_force_en']] = int.to_bytes(CFG_SW_force_EN, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_ch_emul_2']] = int.to_bytes(EMUL_L1_v, 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_ch_emul_3']] = int.to_bytes((EMUL_L0_v<<4)+(EMUL_tau_v<<2)+(EMUL_EN_L1<<1)+(EMUL_EN_L0), 1, 'big')
        self.reg_data[self.registers_metadata_name_to_addr['cfg_ch_emul_4']] = int.to_bytes((EMUL_ADDR_i<<5)+(EMUL_DATA_i), 1, 'big')
        return

    def __str__(self) -> str:
        res = '{\n'
        for i in range(len(self.reg_data)):
            if i not in self.registers_metadata_addr_to_name:
                continue
            res += f'\t"{self.registers_metadata_addr_to_name[i]}":"{int.from_bytes(self.reg_data[i], "big"):08b}",\n'

        return res[:]+'}'
    
    def get_analog_regs(self):
        pass

    def get_analog_digital_regs(self):
        pass

    def get_digital_regs(self):
        pass

    def get_rw_regs(self):
        pass

    def get_r_regs(self):
        pass

reg = RegData()
print(reg)