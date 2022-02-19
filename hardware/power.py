from machine import ADC, Pin
import utime

adc_current = ADC(Pin(26))      # analog value from SCT-013-030 current sesnor
adc_voltage = ADC(Pin(27))      # analog value from ZMPT101B voltage sensor

max_cur = 30                    # at 30A, the current sensor value is 1
max_volt = 120                  # US outlets output at ~120V
volt_div_ratio = 0.5            # external circuit uses 2 10K ohm resistors, bias at middle
trans_reg = 1.2                 # change up or down this value during testing to get right

def calc_volt():
    analog_volt = adc_current.read_u16()                                      # read analog value
    volt_actual = analog_volt * (max_volt * volt_div_ratio) / (5 * trans_reg) # convert to supply voltage
    print("Voltage ADC %d", volt_actual)                                      # print voltage

def calc_cur():
    analog_cur = adc_current.read_u16()                                       # read analog value in 16-bit form
    cur_actual = analog_cur * (max_cur * (3.3 / 1024))                        # convert to supply current
    print("Current ADC: %d", cur_actual)                                      # print current

def main():
    while True:
        calc_cur()
        calc_volt()
        utime.sleep(0.2)


if __name__ == "__main__":
    main()