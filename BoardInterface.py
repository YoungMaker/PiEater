from gpiozero import OutputDevice
import time

#pins:
data_pins = [3, 2, 27, 24, 25, 23, 22, 18]
#data_pins = [18, 22, 23, 24, 25, 27, 2, 3]
data_devices = []

CLK = 11

BUS_EN = 7
RAM_IO = 8
RAM_DIR = 10
RESET = 17
RAM_ADDR = 9

bus_enable  = OutputDevice(BUS_EN, active_high=False, initial_value=True)
ram_io = OutputDevice(RAM_IO, active_high=True, initial_value=False)
ram_en = OutputDevice(RAM_DIR, active_high=True, initial_value=False)
ram_addr = OutputDevice(RAM_ADDR, active_high=False, initial_value=True)
clk = OutputDevice(CLK, active_high=False, initial_value=False)
rst = OutputDevice(RESET, active_high=True, initial_value=False)


def setup_data_pins():
    for pin in data_pins:
        data_devices.append(OutputDevice(pin, active_high=True, initial_value=False))
    data_devices.reverse()

def set_data_bus(integer):
    for x in xrange(0, 7):
        if (integer >> x)&1:
            print 1,
            data_devices[x].on()
        else:
            print 0,
            data_devices[x].off()
    print


# turn all devices off
# place addr on bus
# enable bus
# enable ram_addr
# strobe clock
def write_to_ram_addr(addr, value):
    #clear state
    bus_enable.off()
    ram_io.off()
    ram_en.off()

    #set databus
    set_data_bus(addr)
    bus_enable.on()
    time.sleep(0.002)
    ram_addr.on()

    #toggle clock
    clk.toggle()
    time.sleep(0.002)
    clk.toggle()
    time.sleep(0.002)
    ram_addr.off()

    #put the data value on the bus
    bus_enable.off()
    set_data_bus(value)
    time.sleep(0.005)
    bus_enable.on()

    #strobe the write sequence
    ram_io.on()
    ram_en.on()
    time.sleep(0.01)
    ram_io.off()
    time.sleep(0.01)
    bus_enable.off()
    ram_en.off()



def read_ram_addr(addr):
    #clear state
    bus_enable.off()
    ram_io.off()
    ram_en.off()

    #set databus
    set_data_bus(addr)
    bus_enable.on()
    time.sleep(0.002)
    ram_addr.on()

    #toggle clock
    clk.toggle()
    time.sleep(0.002)
    clk.toggle()
    time.sleep(0.002)
    ram_addr.off()
    bus_enable.off()

    ram_en.on()

if __name__ == '__main__':
    bus_enable.off()
    ram_io.off()
    ram_en.off()
    rst.off()

    #reset the computer
    rst.on()
    time.sleep(0.2)
    rst.off()

    #setup databus pins
    setup_data_pins()

    #write to mem addrs
    for x in xrange(0, 100):
        write_to_ram_addr(x, x+10)

    bus_enable.off()
    #
    while True:
        for x in xrange(0,100):
            read_ram_addr(x)
            time.sleep(10)