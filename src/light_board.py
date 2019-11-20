from fpioa_manager import *
from Maix import FPIOA, GPIO
from machine import UART
from board import board_info

buttons = {}
bt_uart = None

#Main code file for the LED driving board
# Tasks:
# 1) check buttons, BT, ML board for data
# 2) Make decision on mode transfer
# 3) call mode update


# For now, three buttons:
# next, previous, and on/off
#
# next: io6
# prev: io7
# 1/0 : io8
#
def init_buttons():
    next_pin = 6
    prev_pin = 7
    onoff_pin = 8
    fpioa.set_function( next_pin, FPIOA.GPIO6 )
    fpioa.set_function( prev_pin, FPIOA.GPIO7 )
    fpioa.set_function( onoff_pin, FPIOA.GPIO8 )
    next_gpio = GPIO( GPIO.GPIO6, GPIO.IN )
    prev_gpio = GPIO( GPIO.GPIO7, GPIO.IN )
    onoff_gpio = GPIO( GPIO.GPIO8, GPIO.IN )
    return { 'next': next_gpio, 'prev': prev_gpio, 'onoff': onoff_gpio }

def read_buttons():
    reads = {}
    for fcn, gpio in buttons:
        reads[fcn] = gpio.value()
    return reads


# bt uart will run off pins 9(RX) and 10(TX)
def init_bt_uart():
    baud = 9600
    bits = 8
    timeout = 10
    buf_len = 1024
    fm.register( board_info.PIN10, fm.fpioa.UART2_TX, force=True )
    fm.register( board_info.PIN9, fm.fpioa.UART2_RX, force=True )
    return UART( UART.UART2, baud, bits, 0, 0, timeout=timeout, read_buf_len=buf_len )


# returns None if there is no data in the buffer
# otherwise returns any onoff seen
# otherwise returns the last thing recv'd
def read_bt_uart():
    recv = uart.read()
    if res is None:
        return res
    if bytes('0') in recv:
        return bytes('0')
    return recv[-1]

# run off pins 21 (RX) and 22 (TX)
def init_cv_uart():
    fm.register( board_info.PIN21, fm.fpioa.UART1_RX, force=True )
    fm.register( board_info.PIN22, fm.fpioa.UART1_TX, force=True )
    return UART( UART.UART1, 9600, 8, 0, 0, timeout=10, read_buf_len=1024 )

def read_cv_uart():
    recv = uart.read()
    if res is None:
        return res
    if bytes('0') in recv:
        return bytes('0')
    return recv[-1]

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
