/*
 * Return 1 if c is a letter (a-z, A-Z) or a number (0-9).
 */
int isalnum(int c) {
    return (48 <= c && c <= 57)
        || (65 <= c && c <= 90)
        || (97 <= c && c <= 122);
}
