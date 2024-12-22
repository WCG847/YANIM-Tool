from CEKey.core.ce_key import CEKey
import struct


def get_data(limit, output_idx, result_idx, buffer, offset, target):
    """
    Extracts data based on given parameters and updates the buffer with processed data.
    :param limit: The upper limit for data processing.
    :param output_idx: The index to store output data.
    :param result_idx: The index for result data.
    :param buffer: The data buffer to process.
    :param offset: The offset for processing.
    :param target: The target value for processing.
    :return: 0 on completion.
    """
    upper_bound = limit
    output_pointer = output_idx
    result_pointer = result_idx

    search_result = CEKey.search(buffer, offset, target, [0])

    base_offset = 4
    data_offset = search_result << 4
    target_address = base_offset + data_offset

    value1_data = buffer[target_address : target_address + 4]
    if len(value1_data) < 4:
        raise ValueError("Buffer has insufficient bytes to read value1.")
    value1 = struct.unpack(">I", value1_data)[0]

    value2_data = buffer[target_address + 8 : target_address + 12]
    if len(value2_data) < 4:
        raise ValueError("Buffer has insufficient bytes to read value2.")
    value2 = struct.unpack(">I", value2_data)[0]

    if upper_bound < value2:
        struct.pack_into(">I", buffer, result_pointer, -0x100)

    value3_data = buffer[target_address + 4 : target_address + 8]
    if len(value3_data) < 4:
        raise ValueError("Buffer has insufficient bytes to read value3.")
    value3 = struct.unpack(">I", value3_data)[0]

    pointer = target_address + value3
    count = 0

    while pointer < len(buffer):
        byte_value_data = buffer[pointer : pointer + 1]
        if len(byte_value_data) < 1:
            raise ValueError("Buffer has insufficient bytes to read byte value.")
        byte_value = struct.unpack(">B", byte_value_data)[0]

        if byte_value < 0x60:
            break

        next_byte_data = buffer[pointer + 1 : pointer + 2]
        if len(next_byte_data) < 1:
            raise ValueError("Buffer has insufficient bytes to read next byte value.")
        next_byte = struct.unpack(">B", next_byte_data)[0]

        if upper_bound < count:
            break

        struct.pack_into(">B", buffer, output_pointer, next_byte & 0xFF)

        pointer += 2
        count += 1
        count += byte_value - 0x60

    return 0


def check_data(sp_register, ra_register, t0_register, s0_register):
    """
    Checks data based on given register values.
    :param sp_register: Stack pointer register value.
    :param ra_register: Return address register value.
    :param t0_register: Temporary register t0.
    :param s0_register: Saved register s0.
    :return: Result of the search operation.
    """
    sp_register -= 0x30
    ra_saved = ra_register
    s0_saved = s0_register

    search_result = CEKey.search(t0_register, sp_register + 0x2C, ra_register, [0])
    sp_register += 0x30

    return search_result


def check_data_even_more(sp_register, ra_register, t0_register):
    """
    Further checks data with reduced stack pointer offset.
    :param sp_register: Stack pointer register value.
    :param ra_register: Return address register value.
    :param t0_register: Temporary register t0.
    :return: Result of the search operation.
    """
    sp_register -= 0x20
    ra_saved = ra_register

    search_result = CEKey.search(t0_register, sp_register + 0x1C, ra_register, [0])
    sp_register += 0x20

    return search_result


def get_max_sub_rand(a0_register, a1_register):
    """
    Calculates a random value based on provided registers.
    :param a0_register: First input register.
    :param a1_register: Second input register.
    :return: Randomized integer value.
    """
    sp_register = 0x50
    ra_saved = 0x30
    s2_saved = a0_register
    s1_saved = a1_register
    s0_saved = 0

    search_result = CEKey.search(s2_saved, sp_register + 0x4C, a1_register, [0])

    random_value = hash((s0_saved, a0_register, a1_register)) % 0x7FFFFFFF

    sp_register += 0x50

    return random_value


def check_track(a1_register, a2_register, a3_register, t0_register):
    """
    Checks tracking information.
    :param a1_register: Input register 1.
    :param a2_register: Input register 2.
    :param a3_register: Input register 3.
    :param t0_register: Temporary register t0.
    :return: Result of the search operation.
    """
    sp_register -= 0x60
    ra_saved = 0x40

    search_result = CEKey.search(t0_register, sp_register + 0x5C, a1_register, [0])
    sp_register += 0x60

    return search_result


def get_frame_count(file, offset, value):
    sp_register = 0x0  # Initialize sp_register
    sp_register -= 0x30
    ra_saved = 0x10

    # Call CEKey.search with a file object
    search_result = CEKey.search(file, sp_register + 0x2C, value, [0])

    sp_register += 0x30

    return search_result
