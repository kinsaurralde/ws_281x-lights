#ifndef STRUCTS_H
#define STRUCTS_H

#define MAX_LED_PER_STRIP 300
#define LED_STRIP_COUNT 2

class List {
    private:
        unsigned int* data;
        unsigned int length;
        unsigned int counter;
        unsigned int mode;

    public:
        List();
        List(unsigned int length);
        ~List();

        unsigned int size();
        void incrementCounter();
        void decrementCounter();
        void setCounter(int value);
        unsigned int getCounter();
        unsigned int getNext();
        unsigned int getCurrent();
        unsigned int get(unsigned int index);
        void set(unsigned int index, unsigned int value);

        unsigned int operator [](unsigned int i) const;
        unsigned int& operator [](unsigned int i);
};

enum Animation {
    color,
    wipe,
    pulse,
    rainbow,
    cycle,
    randomCycle,
    reverser
};

enum ShiftMode {
    blank_shift,
    first_pixel_shift,
    loop_shift
};

typedef struct {
    unsigned int main[MAX_LED_PER_STRIP];
    unsigned int second[MAX_LED_PER_STRIP];
} Frame;

typedef struct {
    Animation animation;
    int color;
    int color_bg;
    List* colors;
    unsigned int wait_ms;
    unsigned int arg1;
    unsigned int arg2;
    unsigned int arg3;
    int arg4;
    int arg5;
    bool arg6;
    bool arg7;
    bool arg8;
} AnimationArgs;

typedef struct {
    unsigned int arg1;
    unsigned int arg2;
    unsigned int arg3;
    int arg4;
    int arg5;
    bool arg6;
    bool arg7;
    bool arg8;
    List* list;
} IncrementArgs;

void resetIncArgs(IncrementArgs& incArgs, unsigned int nums, bool booleans);

#endif