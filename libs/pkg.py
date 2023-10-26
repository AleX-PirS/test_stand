

class RegData(object):
    reg_data = [int.to_bytes(0, 1, 'big') for _ in range(122)]

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
                 CFG_p2_puls_SOC = 0b01000,
                 CFG_p2_puls_SWM = 0b01010,
                 CFG_p2_puls_EOC = 0b00100,
                 CFG_p3_L1_over = 0b0110_0100_01,
                 CFG_rst_puls_EOC = 0b01000,
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
        
        
        pass

    def __str__(self) -> str:
        res = '{'
        for i in range(len(self.reg_data)):
            res += f'{i}:{int.from_bytes(self.reg_data[i], "big"):#010b}, '

        return res[:-2]+'}'


# reg = RegData()

Hello = 1

print(Hello.__abs__)