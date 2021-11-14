import time
import os


def set_gpio(gpiox):
    gpio_dir = f'/sys/class/gpio/gpio{gpiox}'
    if os.path.isfile(f'{gpio_dir}/value'):
        with open(f'{gpio_dir}/direction') as state:
            if state.read(2) == 'in':
                is_state_out = False
            else:
                is_state_out = True
        if not is_state_out:
            with open(f'{gpio_dir}/direction', 'w') as state:
                state.write('out')
        with open(f'{gpio_dir}/value', 'w') as gpio:
            gpio.write('1')
    else:
        with open(f'/sys/class/gpio/export', 'w') as export:
            export.write(f'{gpiox}')
        set_gpio(gpiox)


def reset_gpio(gpiox):
    gpio_dir = f'/sys/class/gpio/gpio{gpiox}'
    if os.path.isfile(f'{gpio_dir}/value'):
        with open(f'{gpio_dir}/direction') as state:
            if state.read() == 'in':
                is_state_out = False
            else:
                is_state_out = True
        if not is_state_out:
            with open(f'{gpio_dir}/direction', 'w') as state:
                state.write('out')
        with open(f'{gpio_dir}/value', 'w') as gpio:
            gpio.write('0')
    else:
        with open(f'/sys/class/gpio/export', 'w') as export:
            export.write(f'{gpiox}')
        set_gpio(gpiox)


if __name__ == '__main__':
    while True:
        set_gpio(60)
        time.sleep(2)
        set_gpio(61)
        time.sleep(2)
        set_gpio(62)
        time.sleep(2)
        set_gpio(63)
        time.sleep(2)
        reset_gpio(60)
        reset_gpio(61)
        reset_gpio(62)
        reset_gpio(63)
        time.sleep(5)
