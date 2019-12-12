import sensor,image,lcd,time
import KPU as kpu
from machine import UART
from fpioa_manager import fm
from board import board_info

#Initialize pins for UART
fm.register( board_info.PIN10, fm.fpioa.UART2_TX, force=True)
fm.register( board_info.PIN9, fm.fpioa.UART2_RX, force=True)

#Configure UART settings. Some fields are omitted for default settings
uart = UART( UART.UART2, 9600, 8, 0, 0, timeout=10000, read_buf_len=1024 )


lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
classmap = ['dog','sofa', 'cat','bicycle','person','chair','bottle']
classcount = [0,0,0,0,0,0,0,0]
count = 0
task = kpu.load(0x500000)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    print(clock.fps())
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect())
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                #lcd.draw_string(i.x(), i.y()+12, '%f1'%i.value(), lcd.RED, lcd.WHITE)
                if str(classes[i.classid()]) in classmap:
                    classcount[(classmap.index(classes[i.classid()]))]=classcount[(classmap.index(classes[i.classid()]))]+1
                    lcd.draw_string(i.x(), i.y()+12, str(classcount.index(max(classcount))), lcd.BLUE, lcd.WHITE)
    else:
        a = lcd.display(img)
        classcount = [0,0,0,0,0,0,0,0]

    if max(classcount)>4:
        uart.write(str(classcount.index(max(classcount))))
        classcount = [0,0,0,0,0,0,0,0]


a = kpu.deinit(task)
