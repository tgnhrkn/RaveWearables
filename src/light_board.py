from fpioa_manager import *
from Maix import FPIOA, GPIO
from machine import UART
from board import board_info
from modes import *
from Led import *
import lcd

bt_uart = None
cv_uart = None
lstrip = None
n_modes = 4

#Main code file for the LED driving board
# Tasks:
# 1) check buttons, BT, ML board for data
# 2) Make decision on mode transfer
# 3) call mode update

# bt uart will run off pins 9(RX) and 10(TX)
def init_bt_uart():
    baud = 9600
    bits = 8
    timeout = 10
    buf_len = 1024
    fm.register( board_info.PIN10, fm.fpioa.UART2_RX, force=True )
    fm.register( board_info.PIN9, fm.fpioa.UART2_TX, force=True )
    return UART( UART.UART2, baud, bits, 0, 0, timeout=timeout, read_buf_len=buf_len )

# returns None if there is no data in the buffer
# otherwise returns any onoff seen
# otherwise returns the last thing recv'd
def read_bt_uart():
    recv = bt_uart.read()
    if recv is None:
        return None
    
    try:
        recv = recv.decode()
        return int( recv[-1] )
    except:
        return None

# run off pins 17 (RX) and 15 (TX)
def init_cv_uart():
    fm.register( board_info.PIN15, fm.fpioa.UART1_TX, force=True )
    fm.register( board_info.PIN17, fm.fpioa.UART1_RX, force=True )
    return UART( UART.UART1, 9600, 8, 0, 0, timeout=10, read_buf_len=1024 )

def read_cv_uart():
    recv = cv_uart.read()
    if recv is None:
        return None
    
    try:
        recv = recv.decode()
        return int( recv[-1] )
    except:
        return None

def init_leds():
    global lstrip
    lstrip = LedStrip(6, 45)

def init_hw():
    global bt_uart, cv_uart
    bt_uart = init_bt_uart()
    cv_uart = init_cv_uart()
    init_leds()

def init_modes():
    modes = list( [ Mode(lstrip) for _ in range(n_modes) ] )
    modes[0] = OffMode(lstrip) 
    modes[1] = FlashMode(lstrip) 
    modes[2] = MoveAcross(lstrip)
    modes[3] = RainbowCycle(lstrip)
    return modes

def get_control( bt, cv ):
    if bt is not None and ( bt >= 0 and bt < n_modes ):
        return bt
    if cv is not None and ( cv >= 0 and cv < n_modes ):
        return cv
    return None

def run():
    init_hw()
    modes = init_modes()
    curr_mode_idx = 0
    curr_mode = modes[curr_mode_idx]
    curr_mode.enter_mode()

    while True:
        bt_bytes = read_bt_uart()
        cv_bytes = read_cv_uart()
        
        # decide new mode
        new_mode_idx = get_control( bt_bytes, cv_bytes )
        new_mode = None
        if new_mode_idx is not None:
            new_mode = modes[new_mode_idx]

        if new_mode is not None and new_mode != curr_mode:
            curr_mode = new_mode
            curr_mode.enter_mode()
        else:
            curr_mode.update_mode()

run()
