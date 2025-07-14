/*
 * errno defaults to 0 at program start.
 */
static int _errno = 0;

int *__errno_location(void) {
    return &_errno;
}
