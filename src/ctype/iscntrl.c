/*
 * Return 1 if c is a control character (non-printable character: control
 * codes, tab, whitespaces (except space ' '), backspace).
 */
int iscntrl(int c) {
    return (0 <= c && c <= 31) || c == 127;
}
