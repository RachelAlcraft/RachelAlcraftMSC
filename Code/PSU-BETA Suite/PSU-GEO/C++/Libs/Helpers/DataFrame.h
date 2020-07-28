#pragma once
#include <string>
#include <vector>
/*
This prints out a file in a data format for R.
Comma delim with headers
Each row should be an observation
*/

using namespace std;

class DataFrame
{
private:
	string _filename;
public:
	vector<string> headerVector;
	vector<vector<string>> fileVector;
public:
	DataFrame(string filepath);
	void print();
	bool flush();
};

