import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
import logging
import time
import smbus
import RPi.GPIO as GPIO
import max30102

# 配置树莓派的GPIO 空污传感器接在BCM24/23上
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

# 新建一个i2c对象
bus = smbus.SMBus(1)

# 创建一个MODBUS-TCP对象并开启服务
logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
server = modbus_tcp.TcpServer(address="192.168.0.108", port=502)
server.start()

# 添加一个slaver，给这个slaver添加温度、湿度、光照、空气质量的block(Niagara中称为Point)
slaver = server.add_slave(1)
slaver.add_block('Temperature', cst.READ_INPUT_REGISTERS, 185, 1)
slaver.add_block('Humidity', cst.READ_INPUT_REGISTERS, 186, 1)
slaver.add_block('Light', cst.READ_INPUT_REGISTERS, 187, 1)
slaver.add_block('Air', cst.READ_INPUT_REGISTERS, 188, 1)

# 开启光照传感器
bus.write_i2c_block_data(0x39, 0x80, [0x03])

while True:
    # 读取计算SHT30传感器的温湿度
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    # print(data)
    temp = data[0] * 256 + data[1]
    temp = -45 + (175 * temp / 65535.0)
    temp = int(temp * 10)
    humi = 100 * (data[3] * 256 + data[4]) / 65535.0
    humi = int(humi * 10)
    # 更新温度和湿度寄存器的值
    slaver.set_values('Temperature', 185, temp)
    slaver.set_values("Humidity", 186, humi)
    # print(f"temperature:{temp / 10}")
    # print(f"humidity:{humi / 10}")

    # 读取光照传感器的值
    data0_low = bus.read_i2c_block_data(0x39, 0x8c, 1)
    data0_high = bus.read_i2c_block_data(0x39, 0x8d, 1)
    data1_low = bus.read_i2c_block_data(0x39, 0x8e, 1)
    data1_high = bus.read_i2c_block_data(0x39, 0x8f, 1)
    data0 = data0_high[0] * 256 + data0_low[0]
    data1 = data1_high[0] * 256 + data1_low[0]
    if data0 == 0:
        light = 0
    else:
        div = float(data1) / float(data0)
        if 0 < div <= 0.5:
            light = (0.304 * data0 - 0.062 * data0 * (div ** 1.4))
        elif div <= 0.61:
            light = (0.0224 * data0 - 0.031 * data1)
        elif div <= 0.8:
            light = (0.0128 * data0 - 0.0153 * data1)
        elif div <= 1.3:
            light = (0.00146 * data0 - 0.00112 * data1)
        else:
            light = 0
    # print(f"light:{light}")
    # 更新光照寄存器的值
    slaver.set_values('Light', 187, int(light))

    # 读取空污模组的值
    # 空污传感器A脚接在BCM24上，B脚接在BCM23上
    # 空污传感器输出信号定义：
    # 污染等级    A信号输出    B信号输出     污染状态标识
    # 0         Low         Low         优
    # 1         Low         High        良
    # 2         High        Low         中
    # 3         High        High        差

    A = GPIO.input(24)
    B = GPIO.input(23)
    if A == 0 and B == 0:
        air = 0
    elif A == 0 and B == 1:
        air = 1
    elif A == 1 and B == 0:
        air = 2
    else:
        air = 3
    # print(air)
    # 更新空气质量传感器的值
    slaver.set_values('Air', 188, air)

#    m = max30102.MAX30102()
#    red, ir = m.read_sequential()
#    print(red,ir)

    # time.sleep(2)