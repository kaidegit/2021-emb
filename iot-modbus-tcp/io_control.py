import pigpio
import time

tick0, tick1 = None, None


def callback(gpio, level, tick):
    global tick0, tick1

    if level == 0:
        tick0 = tick
        if tick1 is not None:
            diff = pigpio.tickDiff(tick1, tick)
            print(f"High for {diff} ms")
    else:
        tick1 = tick
        if tick0 is not None:
            diff = pigpio.tickDiff(tick0, tick)
            print(f"Low for {diff} ms")


pi = pigpio.pi()

# 使用博通编码
cb = pi.callback(4, pigpio.EITHER_EDGE, callback)
