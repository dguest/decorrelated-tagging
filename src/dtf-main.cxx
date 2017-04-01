

#include <iostream>
#include <fstream>

int main(int argc, char* argv[]) {
  int in = 0;
  if (argc > 1) in = atoi(argv[1]);
  int testint = testfunc(in);
  printf("bonjour et %i\n", testint);
  return 0;
}
