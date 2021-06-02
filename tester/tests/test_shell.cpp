#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include <string>
#include <vector>
// Include the cpp file we're testing
#include "process.cpp"
#include "parser.cpp"

using namespace std;

bool compProcessVecs(const vector<Process*> &v1, const vector<Process*> &v2) {
    if(v1.size() != v2.size()) {
        return false;
    }
    for(int i = 0; i < v1.size(); i++) {
        if(!v1[i]->compare(*v2[i])) {
            return false;
        }
    }
    return true;
}

TEST_CASE("Checking the method that checks Process* arrays", "[classic]") {
    GIVEN("Checking the method that checks Process* arrays"){
        string str = "cmd1";
        vector<Process*> ans1;
        vector<Process*> ans2;
        vector<string> args;
        Process *p1 = new Process("cmd1", args);
        ans1.push_back(p1);
        ans2.push_back(p1);
        CHECK( compProcessVecs(ans1, ans2) );
    }
}
TEST_CASE("One command", "[classic]") {
    GIVEN("One command"){
        string str = "cmd1";
        vector<Process*> ans;
        vector<string> args;
        Process *p1 = new Process("cmd1", args);
        ans.push_back(p1);
        
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("One command plus extra spaces", "[classic]") {
    GIVEN("One command"){
        string str = "cmd1   ";
        vector<Process*> ans;
        vector<string> args;
        Process *p1 = new Process("cmd1", args);
        ans.push_back(p1);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("One command and one argument", "[classic]") {
    GIVEN("One command and one argument"){
        string str = "cmd1 arg1";
        vector<Process*> ans;
        vector<string> args;
        args.push_back("arg1");
        Process *p1 = new Process("cmd1", args);
        ans.push_back(p1);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Two commands with one argument for each", "[classic]") {
    GIVEN("Two commands with one argument for each"){
        string str = "cmd1 arg1 | cmd2 arg2";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1");
        Process *p1 = new Process("cmd1", args1);
        vector<string> args2;
        args2.push_back("arg2");
        Process *p2 = new Process("cmd2", args2);
        ans.push_back(p1);
        ans.push_back(p2);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Extra spaces after args", "[classic]") {
    GIVEN("Extra spaces after args"){
        string str = "cmd1 arg1  ";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1");
        Process *p1 = new Process("cmd1", args1);
        ans.push_back(p1);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Five commands with one argument for each, different spaces and command separation characters", "[classic]") {
    GIVEN("Five commands with one argument for each, different spaces and command separation characters"){
        string str = "cmd1 arg1 | cmd2 arg2<cmd3 arg3> cmd4  arg4 >cmd5 arg5";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1");
        Process *p1 = new Process("cmd1", args1);

        vector<string> args2;
        args2.push_back("arg2");
        Process *p2 = new Process("cmd2", args2);

        vector<string> args3;
        args3.push_back("arg3");
        Process *p3 = new Process("cmd3", args3);

        vector<string> args4;
        args4.push_back("arg4");
        Process *p4 = new Process("cmd4", args4);

        vector<string> args5;
        args5.push_back("arg5");
        Process *p5 = new Process("cmd5", args5);

        ans.push_back(p1);
        ans.push_back(p2);
        ans.push_back(p3);
        ans.push_back(p4);
        ans.push_back(p5);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE(">1 argument and extra ending command delimiter character", "[classic]") {
    GIVEN(">1 argument and extra ending command delimiter character"){
        string str = "cmd1 arg1 arg2 arg3| cmd2 arg4 |";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1");
        args1.push_back("arg2");
        args1.push_back("arg3");
        Process *p1 = new Process("cmd1", args1);
        vector<string> args2;
        args2.push_back("arg4");
        Process *p2 = new Process("cmd2", args2);
        ans.push_back(p1);
        ans.push_back(p2);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Single and double quotes around arguments", "[classic]") {
    GIVEN("Single and double quotes around arguments"){
        string str = "cmd1 \"arg1 arg2 arg3\" | cmd2 \'arg4  arg5\' arg6";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1 arg2 arg3");
        Process *p1 = new Process("cmd1", args1);
        vector<string> args2;
        args2.push_back("arg4  arg5");
        args2.push_back("arg6");
        Process *p2 = new Process("cmd2", args2);
        ans.push_back(p1);
        ans.push_back(p2);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Quotes around command delimiter character", "[classic]") {
    GIVEN("Quotes around command delimiter character"){
        string str = "cmd1 \"arg1 | arg2 <>|<>|<>|<>| arg3\" | cmd2 \'arg4 |\' arg5";
        vector<Process*> ans;
        vector<string> args1;
        args1.push_back("arg1 | arg2 <>|<>|<>|<>| arg3");
        Process *p1 = new Process("cmd1", args1);
        vector<string> args2;
        args2.push_back("arg4 |");
        args2.push_back("arg5");
        Process *p2 = new Process("cmd2", args2);
        ans.push_back(p1);
        ans.push_back(p2);
        CHECK( compProcessVecs(convert_processes(str), ans) );
    }
}
TEST_CASE("Mismatched quotes", "[classic]") {
    GIVEN("Mismatched quotes"){
        string str = "cmd1 \"arg1 | cmd2 arg2";
        try {
            convert_processes(str);
            CHECK(1 == 0); //no exception was thrown
        }
        catch(const char* msg) {
            CHECK( msg == "Exception: mismatched quotes" );
        }
    }
}