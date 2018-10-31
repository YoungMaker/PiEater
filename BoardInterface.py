from gpiozero import OutputDevice
import time

#pins:
data_pins = [3, 2, 27, 24, 25, 23, 22, 18]
#data_pins = [18, 22, 23, 24, 25, 27, 2, 3]
data_devices = []

CLK = 11
PC_LOAD = 4
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
pc_load = OutputDevice(PC_LOAD, active_high=False, initial_value=True)

def setup_data_pins():
    for pin in data_pins:
        data_devices.append(OutputDevice(pin, active_high=True, initial_value=False))
    data_devices.reverse()

def close_data_pins():
    for pin in data_devices:
        pin.close()

def close_pins():
    close_data_pins()
    bus_enable.close()
    ram_io.close()
    ram_en.close()
    ram_addr.close()
    clk.close()
    rst.close()
    pc_load.close()


def set_data_bus(integer):
    for x in xrange(0, len(data_devices)):
        if (integer >> x)&1:
            print 1,
            data_devices[x].on()
        else:
            print 0,
            data_devices[x].off()
    print


def clear_state():
    bus_enable.off()
    ram_io.off()
    ram_en.off()
    ram_addr.off()
    rst.off()
    pc_load.off()

def toggle_clock():
    clk.toggle()
    time.sleep(0.08)
    clk.toggle()
    time.sleep(0.08)

def reset():
    #reset the computer
    rst.on()
    time.sleep(0.2)
    rst.off()

# turn all devices off
# place addr on bus
# enable bus
# enable ram_addr
# strobe clock
# disable ram_addr
# place value on bus
# enable ram_io
# enable ram_en
# disable ram_io
# disable ram_en
def write_to_ram_addr(addr, value):
    clear_state()

    #set databus
    set_data_bus(addr)
    bus_enable.on()
    time.sleep(0.002)
    ram_addr.on()

    toggle_clock()
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
    clear_state()

    #set databus
    set_data_bus(addr)
    bus_enable.on()
    time.sleep(0.002)
    ram_addr.on()

    #toggle clock
    toggle_clock()
    ram_addr.off()
    bus_enable.off()

    ram_en.on()

def show_ram_addr_cont(addr):
    clear_state()

    #set databus
    set_data_bus(addr)
    bus_enable.on()
    time.sleep(0.002)
    ram_addr.on()

    #toggle clock
    toggle_clock()
    ram_addr.off()
    bus_enable.off()

    ram_en.off()

def set_prog_ctr_value(value):
    clear_state()

    #set databus
    set_data_bus(value)
    bus_enable.on()
    time.sleep(0.002)
    #set load
    pc_load.on()
    #toggle clock
    toggle_clock()
    pc_load.off()
    bus_enable.off()

if __name__ == '__main__':
    clear_state()
    reset()

    #setup databus pins
    setup_data_pins()

    set_prog_ctr_value(0x06)


    # #write to mem addrs
    # for x in xrange(0, 100):
    #     write_to_ram_addr(x, x+10)
    #
    # bus_enable.off()
    # #
    # while True:
    #     for x in xrange(0,100):
    #         read_ram_addr(x)
    #         time.sleep(10)



    close_pins()
