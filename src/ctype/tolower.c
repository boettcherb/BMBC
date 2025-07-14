/*
 * If c is an uppercase letter, convert it to a lowercase letter.
 */
int tolower(int c) {
    return (65 <= c && c <= 90) ? c + 32 : c;
}
