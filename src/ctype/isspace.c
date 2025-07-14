/*
 * Return 1 if c is a space (space, tab, new line, carriage return).
 */
int isspace(int c) {
    return (9 <= c && c <= 13) || c == 32;
}
