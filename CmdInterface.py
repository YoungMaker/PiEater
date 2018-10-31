import BoardInterface

def value_in_range(value, start, end):
    if value < start or value > end:
        print "Value '{}' out of range".format(value)
        return False
    return True

def print_help():
    print "Commands: "
    print "\t bus <value> writes <value> onto the databus"
    print "\t reset resets the computer"
    print "\t pc <value> sets a value into the program counter"
    print "\t write <addr> <value> writes a value into the memory address"
    print "\t clk <rate>. Begins clocking the computer at the specified rate. Default rate is 2 Hz"

if __name__ == '__main__':
    BoardInterface.clear_state()
    BoardInterface.reset()
    BoardInterface.setup_data_pins()
    
    while True:

        cmd_input = raw_input("> ")
        
        cmd_input.strip()
        split_cmds = cmd_input.split(" ")
        #print split_cmds

        main_option = split_cmds.pop(0)

        if main_option == "quit" or main_option == "q" or main_option == "exit":
            BoardInterface.clear_state()
            print "bye!"
            break

        if main_option == "help" or main_option == "-h" or main_option == "h":
            print "Commands: "
            print "\t bus|b <value>: writes <value> onto the databus"
            print "\t reset|r: resets the computer"
            print "\t bus|b <on/off>: enables data bus"
            print "\t pc|p <value>: sets a value into the program counter"
            print "\t write|w <addr> <value>: writes a value into the memory address"
            print "\t clk|c <rate>: begins clocking the computer at the specified rate. Default rate is 2 Hz"
            print "\t read|r <addr>: sets the ram address pointer to the specified address" 
            print "\t step|s: toggles the clock once" 

        elif main_option == "reset" or main_option == "r":
            BoardInterface.reset()
            print "pc reset"
        
        elif main_option == "step" or main_option == "s":
            BoardInterface.toggle_clock()
            print "clked" 

        if len(split_cmds) < 1:
            continue

        elif main_option == "bus" or main_option == "b":
            pop_val = split_cmds.pop(0)
            if pop_val == "on":
                print "Turning on the bus controller"
                BoardInterface.bus_enable.on()
                continue
                
            elif pop_val == "off":
                print "Turning off the bus controller"
                BoardInterface.bus_enable.off()
                continue

            try:
                value = int(pop_val)
                if not value_in_range(value, 0, 255): continue

                print "Writing value {} to bus".format(value)
                BoardInterface.set_data_bus(value)
            except ValueError:
                print "Invalid argument. Must be 8 bit integer (0-255)"

        elif main_option == "write" or main_option == "w":
            if len(split_cmds) < 2:
                print "Invalid arguments. Usage: write <addr> <value> writes a value into the memory address"
                continue

            try:
                addr = int(split_cmds.pop(0))
                if not value_in_range(addr, 0, 255): continue

                value = int(split_cmds.pop(0))
                if not value_in_range(addr, 0, 255): continue

                BoardInterface.write_to_ram_addr(addr, value)
            except ValueError:
                print "Invalid argument. Must be 8 bit integer (0-255)"
        
        elif main_option == "read" or main_option == "r":
            try:
                value = int(split_cmds.pop(0))
                if not value_in_range(value, 0, 255): continue

                print "reading from addr {}".format(value)
                BoardInterface.show_ram_addr_cont(value) 
            except ValueError:
                print "Invalid argument. Must be 8 bit integer (0-255)"


        elif main_option == "pc" or main_option =="p":
            try:
                value = int(split_cmds.pop(0))
                if not value_in_range(value, 0, 255): continue


                print "Writing value {} to program counter".format(value)
                BoardInterface.set_prog_ctr_value(value)
            except ValueError:
                print "Invalid argument. Must be 8 bit integer (0-255)"

        # elif main_option == "clk":
        #     if len(split_cmds) > 0:
        #         try:
        #             value = float(split_cmds.pop(0))
        #             if value < 0.1 or value > 10:
        #                 print "Invalid argument. Must be floating point 0.1 - 10Hz"
        #                 continue
        #
        #             print "Clocking at {}Hz".format(value)
        #         except ValueError:
        #             print "Invalid argument. Must be floating point 0.1 - 10Hz"
        #             continue
        #     else:
        #         print "Clocking at 2Hz"

        else:
            print "command '" + main_option + "' was not recognized"
