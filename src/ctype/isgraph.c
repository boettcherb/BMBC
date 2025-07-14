/*
 * Return 1 if c is graphic (ie. visible): letters, numbers, punctuation.
 */
int isgraph(int c) {
    return 33 <= c && c <= 126;
}
