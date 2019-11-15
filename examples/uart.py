import time
from machine import UART
from fpioa_manager import fm
from board import board_info

# This example uses the HC05, and pins 10 for TX, 9 for RX

fm.register( board_info.PIN10, fm.fpioa.UART2_TX, force=True)
fm.register( board_info.PIN9, fm.fpioa.UART2_RX, force=True)

uart = UART( UART.UART2, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096 )

time.sleep(1)

uart.write( "You are running the uart example script!\r\n" )
uart.write( "Type some stuff and it will be echoed back!\r\n" )
uart.write( "Press enter to quit...\r\n" )

while True:
    res = uart.read()
    if res is not None:
        if 0x7f in res:
            break;
        uart.write( res )

uart.write( "Finished\r\n" )

