#ifndef __CLASS1_H__
#define __CLASS1_H__

#include <vector>
#include <string>

using namespace std;

class Class1{
public:
    Class1(string cmd, vector<string> args);
    ~Class1();
    Class1(const Class1 &copyMe);
    operator std::string() const;
    bool compare(const Class1 &other);
    friend std::ostream& operator<<(std::ostream&, const Class1&);
private:
    string command;
    vector<string> arguments;
};

#endif
