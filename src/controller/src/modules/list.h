#ifndef SRC_MODULES_LIST_H_
#define SRC_MODULES_LIST_H_

#include <cstdint>
#include <cstring>

#include "../../config.h"

class List {
 public:
  List() : counter_(0), size_(0) { memset(&items_, 0, LIST_CAPACITY * sizeof(uint32_t)); }

  void reset();
  void setSize(int value);
  int size() const;
  int counter() const;
  void increment();
  void decrement();
  void set(int index, uint32_t value);
  uint32_t get(int index);
  uint32_t getCurrent();
  uint32_t getNext();

 private:
  uint32_t items_[LIST_CAPACITY];
  int counter_;
  int size_;

  static bool isValidIndex(int index);
};

#endif  // SRC_MODULES_LIST_H_
