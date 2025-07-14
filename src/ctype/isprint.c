/*
 * Return 1 if c is printable: letters, numbers, punctuation, space.
 */
int isprint(int c) {
    return 32 <= c && c <= 126;
}
