/*
 * Return 1 if c is a hexadecimal digit (0-9, A-F, a-f), and 0 otherwise.
 */
int isxdigit(int c) {
    return (48 <= c && c <= 57)
        || (65 <= c && c <= 70)
        || (97 <= c && c <= 102);
}
