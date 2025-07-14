/*
 * Return 1 if c is a punctuation mark.
 */
int ispunct(int c) {
    return (33 <= c && c <= 47)
        || (58 <= c && c <= 64)
        || (91 <= c && c <= 96)
        || (123 <= c && c <= 126);
}
