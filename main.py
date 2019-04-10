import serial, time
from fn import readFile, readPort, parsGCode, makeSlicerCommand
import sys
from os import system
port_ = "/dev/ttyUSB0"
baudrate_ = 19200
printer = serial.Serial(port_)
# printer.port = port_
printer.baudrate = baudrate_
printer.timeout = 3

print(printer.name)

# gcode = ['G28', 'G21', 'G90', 'G1 Z5 F 2500', 'G1 X20', 'G1 Y20', 'G1 X30', 'G1 Y30', 'G1 X0 Y0']
# gcode = ['G28', 'G1 X5']
# gcode = parsGCode('test1.gcode', 'file')

system(makeSlicerCommand(sys.argv[1]))

gcode = parsGCode(sys.argv[1].replace('.stl', '.gcode'), 'file')

expectGCode = 'M107'
expectGCode = ''

time.sleep(3)

# printer.write(b'G28\n')

x_ = "b'ok\n"
count = 0
len_ = len(gcode)
for i in gcode:
    while " \n" in i:
        i = i.replace(" \n", "\n")
    # i = i.replace("\n", "")

    while not("ok" in x_):
        try:
            time.sleep(0.002)
            x_ = str(printer.readline())
            print(x_)
        except Exception as e:
            print(e)
    # printer.write((i+'\n').encode())
    printer.write(i.encode())
    print(i)
    if i[:3] in expectGCode:
        x_ = 'ok'
        print('except!!')
    else:
        x_ = ''
    count += 1
    print("Progress:" + (str(count / len_ * 100)) + "%\n")
    # time.sleep(1)

# M114 - coordinates
# M105 - temp


i = ''
while False:
    allmeta = ''
    gc_ = 0
    try:
        meta = printer.readline()
        allmeta += meta
        if 'ok' in allmeta:
            allmeta = ''
            sendGCode = bytes(gcode[gc_]+"\n")
            printer.write(sendGCode)
            print(sendGCode)
            gc_ += 1
            if gc_ == len(gcode_):
                gc_ = 0
                break
        time.sleep(0.5)
    except Exception as e:
        print('ERROR!!\n\t', e)
    print(meta)
    # print(readPort(printer), end = '')
