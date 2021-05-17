# the first version of system dictionaries
SYSTEM_DICT_VERSION_1 = 0xeb5b87cc8b3f406c


def is_dictionary(version):
    """Returns ``True`` if, and only if, the file is a system dictionary.

    Args:
        version (int): a dictionary version ID

    Returns:
        bool: ``True`` if the file is a system dictionary, otherwise ``False``
    """
    return version == SYSTEM_DICT_VERSION_1
