#include <fcntl.h>
#include <stdio.h>

void main() {
    struct stat sb;
    printf("%d\n", sizeof(struct stat));
    printf("%d\n", (long)&sb.st_size - (long)&sb);
}
