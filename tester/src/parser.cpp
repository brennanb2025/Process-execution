#include "parser.h"
#include<iostream>
#include<string>
#include<cstring>
#include<cstddef>
#include<cstring>
#include<vector>
using namespace std;

std::string capitalize( const char * const s) {
    std::string rtn;
    bool period = false;
    const char *it = s;
    while( *it != '/0') {
        char c = *it;
        if (c == '.') {
            period = true;
        } else if(period == true) {
            c = toupper(c);
            period = false;
        }
        rtn += c;
        it++;
    }
    return rtn;
}