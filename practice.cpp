#include <cstddef>
#include <iostream>

class IntArray {
 public:
  using data_type = int;
  using size_type = size_t;
  using reference = data_type&;

  IntArray() = default;
  IntArray(size_t n) : array_size(n) {
    int_array = new data_type[n]();
  }
  ~IntArray() {
    delete[] int_array;
    int_array = nullptr;
  }
  IntArray(const IntArray& other) {
    size_t size = other.size();
    int_array = new data_type[size];
    for (size_t i = 0; i < size; ++i) {
      int_array[i] = other.int_array[i];
    }
  }
  IntArray& operator=(IntArray& other) {
    if (this == &other) {
      return;
    }
    size_t size = other.size();
    delete[] int_array;
    int_array = new data_type[size];
    for (size_t i = 0; i < size; ++i) {
      int_array[i] = other.int_array[i];
    }
  }
  reference operator[](size_t n) {
    return int_array[n];
  }
  const size_type size() const {
    return array_size;
  }

  data_type* int_array{nullptr};
  size_type array_size{0};
};

int main(void) {
  IntArray a(3);
  IntArray b(a);
  a[0] = 1;
  std::cout << b[0] << '\n';
  IntArray c;
}