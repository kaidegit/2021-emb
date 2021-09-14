# 2021-emb

main.py为运行在龙芯派上的收集程序，负责通过modbus-tcp读取树莓派等下位机的数据

iot-modbus-tcp为运行在树莓派等设备上的程序，负责通过i2c等协议读取传感器数据，再通过modbus-tcp给收集器提供数据
