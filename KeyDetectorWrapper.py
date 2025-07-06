import os
import ctypes

dll_path = os.path.abspath('./DLLs/KeyDetectorDLL.dll')
keyDetectorDLL = ctypes.CDLL(dll_path)

def getKey() -> int:
    """
    Retrieves a key press event using the KeyDetectorDLL.

    This function calls the `get_key` method from the KeyDetectorDLL to detect
    if a key has been pressed. It returns the key code of the pressed key,
    or -1 if no key press is detected.

    Returns:
        int: The key code of the pressed key, or -1 if no key press is detected.
    """
    return keyDetectorDLL.get_key()
