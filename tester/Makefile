SRCDIR = src
OBJSDIR = build
INCLUDESDIR = include
TESTDIR = tests

SOURCES = parser.cpp main.cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = shell

CXX = g++
CXXFLAGS = -Wall -g -I$(INCLUDESDIR)

all: directories shell

directories:
	mkdir -p $(OBJSDIR)

# Create the program binary
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o shell \
			$(OBJSDIR)/*.o

# Compile rules for each dependecy
main.o: $(SRCDIR)/main.cpp
	$(CXX) $(CXXFLAGS) -c -o $(OBJSDIR)/main.o $(SRCDIR)/main.cpp
	
parser.o: $(SRCDIR)/parser.cpp $(SRCDIR)/parser.cpp
	$(CXX) $(CXXFLAGS) -c -o $(OBJSDIR)/parser.o $(SRCDIR)/parser.cpp

# Make the test_runner
test: $(TESTDIR)/test_shell.cpp
	$(CXX) $(CXXFLAGS) -Isrc/ -o test_runner $(TESTDIR)/test_*.cpp

# Rule to clean up intermediate file and executable
clean:
	rm -rf $(OBJSDIR)
	rm -f shell test_runner *.o
	
