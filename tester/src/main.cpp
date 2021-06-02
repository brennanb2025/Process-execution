#include<iostream>
#include <unistd.h>
#include <cstdlib>
#include <signal.h>
#include "parser.h"
#include "class1.h"
using namespace std;

void signal_callback_handler(int signum) { //handling ctrl+c
   cout <<  "Shell  Exiting..." << endl;
   // Terminate program
   exit(signum);
}

// C++ Program begins execution here
int main( int argc, char* argv[] ){
    
}
