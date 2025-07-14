/*
 * If c is a lowercase letter, convert it to an uppercase letter.
 */
int toupper(int c) {
    return (97 <= c && c <= 122) ? c - 32 : c;
}
