#include <stdlib.h>
#include <string.h>

#include "structs.h"

#if defined (__AVR__)
    #include <Arduino.h>
#else
    #include <stdio.h>
    #include <iostream>
#endif


List::List() {
    counter = 0;
    length = 1;
    data = (unsigned int*) malloc(length * sizeof(unsigned int));
    data[0] = 0;
    mode = 0;
}

List::List(unsigned int length) : length(length) {
    data = (unsigned int*) malloc(length * sizeof(unsigned int));
    memset(data, 0, length * sizeof(unsigned int));
    counter = 0;
    mode = 0;
}

List::~List() {
    if (data) {
        free(data);
    }
}

unsigned int List::size() {
    return length;
}

void List::incrementCounter() {
    counter = (counter + 1) % length;
}

void List::decrementCounter() {
    counter = (counter - 1 + length) % length;
}

void List::setCounter(int value) {
    counter = (value + length) % length;
}

unsigned int List::getCounter() {
    return counter;
}

unsigned int List::getNext() {
    counter = (counter + 1) % length;
    return data[counter];
}

unsigned int List::getCurrent() {
    return data[counter];
}

unsigned int List::get(unsigned int index) {
    return data[index];
}

void List::set(unsigned int index, unsigned int value) {
    data[index] = value;
}

unsigned int List::operator [](unsigned int i) const {
    if (i >= length) {
        return 0;
    }
    return data[i];
}

unsigned int& List::operator [](unsigned int i)  {
    return data[i];
}

void resetIncArgs(IncrementArgs& incArgs, unsigned int nums = 0, bool booleans = false) {
    incArgs.arg1 = nums;
    incArgs.arg2 = nums;
    incArgs.arg3 = nums;
    incArgs.arg4 = nums;
    incArgs.arg5 = nums;
    incArgs.arg6 = booleans;
    incArgs.arg7 = booleans;
    incArgs.arg8 = booleans;
    delete incArgs.list;
    incArgs.list = new List();
}
