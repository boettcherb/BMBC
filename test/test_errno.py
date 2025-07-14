import ctypes
import subprocess
import pytest
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent / "src" / "errno"
BUILD_DIR = BASE_DIR / "build"
ERRNO_C = SRC_DIR / "errno.c"
ERRNO_SO = BUILD_DIR / "errno.so"

@pytest.fixture(scope="module", autouse=True)
def build_errno_lib():
    BUILD_DIR.mkdir(exist_ok=True)
    subprocess.run(
        ["gcc", "-shared", "-fPIC", "-o", str(ERRNO_SO), str(ERRNO_C)],
        check=True
    )
    yield
    ERRNO_SO.unlink()
    BUILD_DIR.rmdir()


@pytest.fixture(scope="module")
def lib():
    return ctypes.CDLL(str(ERRNO_SO))


def test_errno_initially_zero(lib):
    """errno should be zero on startup"""
    errno_ptr = lib.__errno_location
    errno_ptr.restype = ctypes.POINTER(ctypes.c_int)
    assert errno_ptr().contents.value == 0


def test_errno_read_write(lib):
    """errno should be writable and readable via macro and pointer"""
    errno_ptr = lib.__errno_location
    errno_ptr.restype = ctypes.POINTER(ctypes.c_int)

    ptr = errno_ptr()
    ptr.contents.value = 123
    assert ptr.contents.value == 123

    # Write a different value
    ptr.contents.value = 456
    assert ptr.contents.value == 456


def test_errno_pointer_consistency(lib):
    """errno pointer should be stable"""
    errno_ptr = lib.__errno_location
    errno_ptr.restype = ctypes.POINTER(ctypes.c_int)

    p1 = errno_ptr()
    p2 = errno_ptr()
    assert ctypes.addressof(p1.contents) == ctypes.addressof(p2.contents)


def test_errno_independence(lib):
    """Modifying errno shouldn't affect local variables"""
    errno_ptr = lib.__errno_location
    errno_ptr.restype = ctypes.POINTER(ctypes.c_int)

    x = 42
    errno_ptr().contents.value = 999
    assert x == 42  # sanity check

