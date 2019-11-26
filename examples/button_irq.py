import utime
from Maix import GPIO
def test_irq(GPIO,pin_num):
    print("key",pin_num,"\n")

fm.register(board_info.BOOT_KEY,fm.fpioa.GPIOHS0)
key=GPIO(GPIO.GPIOHS0,GPIO.IN,GPIO.PULL_NONE)
utime.sleep_ms(500)
key.value()
key.irq(test_irq,GPIO.IRQ_BOTH,GPIO.WAKEUP_NOT_SUPPORT,7)

while True:
    pass
