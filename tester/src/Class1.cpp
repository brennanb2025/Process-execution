#include "class1.h"
#include<iostream>
#include<string>
#include<cstring>
#include<cstddef>
#include<cstring>
using namespace std;

Class1::Class1(string cmd, vector<string> args){
    string command;
    vector<string> arguments;
    this->command = cmd;
    this->arguments = args;
};

Class1::Class1(const Class1& copyMe) {
    command = copyMe.command;
    arguments = copyMe.arguments;
};

Class1::~Class1(){};

bool Class1::compare(const Class1 &other) {
    if(command != other.command) {
        return false;
    }
    if(other.arguments.size() != arguments.size()) {
        return false;
    }
    for(int i = 0; i < other.arguments.size(); i++) {
        if(other.arguments[i] != arguments[i]) {
            return false;
        }
    }
    return true;
};

Class1::operator std::string() const { 
    string rtn;
    rtn += "Command: " + command + "\nArguments:\n";
    for(int i = 0; i < arguments.size(); i++) {
        rtn += to_string(i);
        rtn += (": " + arguments[i] + "\n");
    }
    return rtn;
};

std::ostream& operator<<(std::ostream& os, const Class1& obj)
{
   os << static_cast<string>(obj);
   return os;
}