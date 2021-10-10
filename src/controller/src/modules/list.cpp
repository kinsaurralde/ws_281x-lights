#include "list.h"

void List::reset() {
  size_ = 0;
  counter_ = 0;
  memset(items_, 0, LIST_CAPACITY * sizeof(uint32_t));
}

void List::setSize(int value) {
  if (isValidIndex(size_)) {
    size_ = value;
  } else {
    size_ = LIST_CAPACITY;
  }
}

int List::size() const { return size_; }

int List::counter() const { return counter_; }

void List::increment() { counter_ = (counter_ + 1) % size_; }

void List::decrement() { counter_ = (counter_ - 1 + size_) % size_; }

void List::set(int index, uint32_t value) {
  if (isValidIndex(index)) {
    items_[index] = value;
  }
}

uint32_t List::get(int index) {
  if (isValidIndex(index)) {
    return items_[index];
  }
  return 0;
}

uint32_t List::getCurrent() { return items_[counter_]; }

uint32_t List::getNext() {
  increment();
  return items_[counter_];
}

bool List::isValidIndex(int index) { return index >= 0 && index < LIST_CAPACITY; }
