def read_sensor_A1():
    # ADS1115: A1 gegen GND
    config = [0xD3, 0x83]
    bus.write_i2c_block_data(ADS_ADDRESS, CONFIG_REGISTER, config)
    time.sleep(0.001)

    data = bus.read_i2c_block_data(ADS_ADDRESS, CONVERSION_REGISTER, 2)
    value = (data[0] << 8) | data[1]

    if value > 32767:
        value -= 65536

    return value + 32768

def read_sensor_A2():
    # ADS1115: A2 gegen GND
    config = [0xE3, 0x83]
    bus.write_i2c_block_data(ADS_ADDRESS, CONFIG_REGISTER, config)
    time.sleep(0.001)

    data = bus.read_i2c_block_data(ADS_ADDRESS, CONVERSION_REGISTER, 2)
    value = (data[0] << 8) | data[1]

    if value > 32767:
        value -= 65536

    return value + 32768

def read_sensor_A3():
    # ADS1115: A3 gegen GND
    config = [0xF3, 0x83]
    bus.write_i2c_block_data(ADS_ADDRESS, CONFIG_REGISTER, config)
    time.sleep(0.001)

    data = bus.read_i2c_block_data(ADS_ADDRESS, CONVERSION_REGISTER, 2)
    value = (data[0] << 8) | data[1]

    if value > 32767:
        value -= 65536

    return value + 32768