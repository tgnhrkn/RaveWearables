# Main code file for the LED driving board
# Tasks:
# 1) check buttons, BT, ML board for data
# 2) Make decision on mode transfer
# 3) call mode update

def init_buttons():
    return False

def read_buttons():
    return []

def init_bt_uart():
    return False

def read_bt_uart():
    return []

def init_cv_uart():
    return False

def read_cv_uart():
    return []

def init_leds():
    return False

def init_hw():
    init_buttons()
    init_bt_uart()
    init_cv_uart()

def init_modes():
    modes = []
    modes.append( Mode() )
    return modes

def run():
    init_hw()
    modes = init_modes()
    curr_mode_idx = 0
    curr_mode = modes[curr_mode_idx]

    while True:
        read_buttons()
        read_bt_uart()
        read_cv_uart()
        
        # decide new mode
        new_mode = None

        if new_mode is not None and new_mode != curr_mode:
            curr_mode = new_mode
            curr_mode.enter_mode()
        else:
            curr_mode.update_mode()

run()
