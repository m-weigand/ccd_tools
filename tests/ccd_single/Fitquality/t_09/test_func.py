from lib_dd.test_functions import *


def test_regressions(old_result, new_result):
    t_rms_pos_change(old_result, new_result, allowed_percentage=0.1)
