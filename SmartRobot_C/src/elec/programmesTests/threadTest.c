#include <pthread.h>
#include <stdio.h>

// gcc -o thread thread.c -lpthread

void* foo(void* arg) {
    printf("foo \n");
    pthread_exit(NULL);
    return NULL;
}

int main(void) {
    // type du thread
    pthread_t tid1;

    // creation du thread
    pthread_create(&tid1, NULL,foo, NULL);

    // attend la fin du thread (pthread exit)
    pthread_join(tid1, NULL);

    return 0;
}