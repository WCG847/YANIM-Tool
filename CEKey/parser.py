from CEKey.core.ce_key import CEKey
from CEKey.core.processor import (
    get_data,
    check_data,
    check_data_even_more,
    get_max_sub_rand,
    check_track,
    get_frame_count,
)


class YMKs:
    CEKey = CEKey

    @staticmethod
    def GetData(limit, output_idx, result_idx, buffer, offset, target):
        return get_data(limit, output_idx, result_idx, buffer, offset, target)

    @staticmethod
    def CheckData(sp_register, ra_register, t0_register, s0_register):
        return check_data(sp_register, ra_register, t0_register, s0_register)

    @staticmethod
    def CheckDataEvenMore(sp_register, ra_register, t0_register):
        return check_data_even_more(sp_register, ra_register, t0_register)

    @staticmethod
    def GetMaxSubRand(a0_register, a1_register):
        return get_max_sub_rand(a0_register, a1_register)

    @staticmethod
    def CheckTrack(a1_register, a2_register, a3_register, t0_register):
        return check_track(a1_register, a2_register, a3_register, t0_register)

    @staticmethod
    def GetFrameCount(a0_register, a1_register, a2_register):
        return get_frame_count(a0_register, a1_register, a2_register)