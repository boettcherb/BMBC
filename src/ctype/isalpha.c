/*
 * Return 1 if c is a letter (a-z, A-Z).
 */
int isalpha(int c) {
    return (65 <= c && c <= 90) || (97 <= c && c <= 122);
}
