import time

import modbus_tk
import modbus_tk.hooks as hooks
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
import logging

logger = modbus_tk.utils.create_logger("console", level=logging.DEBUG)


def on_after_recv(data):
    master, bytes_data = data
    logger.info(bytes_data)


hooks.install_hook('modbus.Master.after_recv', on_after_recv)


def on_before_connect(args):
    master = args[0]
    logger.debug("on_before_connect {0} {1}".format(master._host, master._port))


hooks.install_hook("modbus_tcp.TcpMaster.before_connect", on_before_connect)


def on_after_recv(args):
    response = args[1]
    logger.debug("on_after_recv {0} bytes received".format(len(response)))


hooks.install_hook("modbus_tcp.TcpMaster.after_recv", on_after_recv)

master = modbus_tcp.TcpMaster(host="192.168.123.39")
master.set_timeout(5.0)
logger.info("connected")
while True:
    temp = master.execute(1, cst.READ_INPUT_REGISTERS, 185, 1)[0] / 10
    humi = master.execute(1, cst.READ_INPUT_REGISTERS, 186, 1)[0] / 10
    light = master.execute(1, cst.READ_INPUT_REGISTERS, 187, 1)[0]
    air = master.execute(1, cst.READ_INPUT_REGISTERS, 188, 1)[0]
    time.sleep(1)
