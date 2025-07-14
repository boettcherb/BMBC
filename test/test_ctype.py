import ctypes
import subprocess
import pytest
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent / "src" / "ctype"
BUILD_DIR = BASE_DIR / "build"

# Map of test names to source filenames and expected valid characters
CTYPE_TESTS = {
    "isalnum": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "isalpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "isblank": " \t",
    "iscntrl": "".join(chr(i) for i in range(32)) + chr(127),
    "isdigit": "0123456789",
    "isgraph": "".join(chr(i) for i in range(33, 127)),
    "islower": "abcdefghijklmnopqrstuvwxyz",
    "isprint": "".join(chr(i) for i in range(32, 127)),
    "ispunct": "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~",
    "isspace": " \t\n\r\v\f",
    "isupper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "isxdigit": "0123456789abcdefABCDEF",
}

@pytest.fixture(scope="module", autouse=True)
def setup_build_dir():
    """Create a temporary build directory and clean it up after tests."""
    BUILD_DIR.mkdir(exist_ok=True)
    yield
    for so_file in BUILD_DIR.glob("*.so"):
        so_file.unlink()
    BUILD_DIR.rmdir()


def compile_shared_lib(name: str) -> Path:
    """Compile the given C file to a shared object (.so) and return its path."""
    src = SRC_DIR / f"{name}.c"
    so = BUILD_DIR / f"{name}.so"
    subprocess.run(["gcc", "-shared", "-o", str(so), "-fPIC", str(src)], check=True)
    return so


@pytest.mark.parametrize("func_name", CTYPE_TESTS.keys())
def test_ctype_function(func_name):
    """Generic test for ctype-like functions."""
    valid_chars = CTYPE_TESTS[func_name]
    so_path = compile_shared_lib(func_name)
    lib = ctypes.CDLL(str(so_path))

    c_func = getattr(lib, func_name)
    c_func.argtypes = [ctypes.c_int]
    c_func.restype = ctypes.c_int

    for i in range(-10, 300):
        expected = 0
        try:
            ch = chr(i)
            expected = 1 if ch in valid_chars else 0
            ch_repr = repr(ch)
        except ValueError:
            ch_repr = f"<invalid chr({i})>"
        assert c_func(i) == expected, f"{func_name} failed for {i} ({ch_repr}), hex: {hex(i)})"


def test_toupper():
    """Test the toupper function."""
    so_path = compile_shared_lib("toupper")
    lib = ctypes.CDLL(str(so_path))
    c_toupper = lib.toupper
    c_toupper.argtypes = [ctypes.c_int]
    c_toupper.restype = ctypes.c_int

    for i in range(-10, 300):
        expected = i
        if 97 <= i <= 122:
            expected = i - 32
        assert c_toupper(i) == expected, f"toupper failed for {chr(i)}, hex: {hex(i)})"


def test_tolower():
    """Test the tolower function."""
    so_path = compile_shared_lib("tolower")
    lib = ctypes.CDLL(str(so_path))
    c_tolower = lib.tolower
    c_tolower.argtypes = [ctypes.c_int]
    c_tolower.restype = ctypes.c_int

    for i in range(-10, 300):
        expected = i
        if 65 <= i <= 90:
            expected = i + 32
        assert c_tolower(i) == expected, f"tolower failed for {chr(i)}"