SYSTEM_DICT_VERSION_1 = 0xeb5b87cc8b3f406c


def is_dictionary(version):
    """

    :param int version:
    :return:
    :rtype: bool
    """
    return version == SYSTEM_DICT_VERSION_1
