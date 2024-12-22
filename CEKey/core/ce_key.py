import struct


class CEKey:
    YTOC_COUNT_OFFSET = 0x100
    YTOC_OFFSET = 0x104

    def __init__(self, data_pointer):
        self.pointer = data_pointer

    def __del__(self):
        pass

    @staticmethod
    def search(file, offset, value, result):
        """
        Searches for a specific value in the file using a binary search algorithm.
        :param file: The file-like object to search.
        :param offset: The offset to start the search.
        :param value: The value to search for.
        :param result: A list to store the result index.
        :return: 1 if the value is found, otherwise 0.
        """
        buffer = bytearray(4)

        initial_value = 0x0001
        bit_mask_7 = (initial_value << 7) & 0xFF
        bit_mask_6 = (initial_value << 6) & 0xFF

        buffer[3] = (buffer[3] & 0x7F) | bit_mask_7
        buffer[3] = (buffer[3] & 0xBF) | bit_mask_6

        buffer[1] = value & 0xFF
        buffer[0] = offset & 0xFF

        temp_value = struct.unpack(">H", buffer[2:4])[0]
        temp_value = (temp_value & ~0x3FFF) | (offset & 0x3FFF)
        struct.pack_into(">H", buffer, 2, temp_value)

        packed_value = struct.unpack(">I", buffer)[0]

        file.seek(CEKey.YTOC_COUNT_OFFSET)
        num_entries_data = file.read(4)
        if len(num_entries_data) < 4:
            raise ValueError(
                "File has insufficient data to read the number of entries."
            )
        num_entries = struct.unpack(">I", num_entries_data)[0]

        left, right = 0, num_entries - 1
        while left <= right:
            mid_index = (left + right) // 2

            file.seek(CEKey.YTOC_OFFSET + (mid_index * 16))
            current_value_data = file.read(4)
            if len(current_value_data) < 4:
                raise ValueError("File has insufficient data to read entry value.")
            current_value = struct.unpack(">I", current_value_data)[0]

            if current_value == packed_value:
                result[0] = mid_index
                return 1
            elif current_value < packed_value:
                left = mid_index + 1
            else:
                right = mid_index - 1

        result[0] = left
        return 0