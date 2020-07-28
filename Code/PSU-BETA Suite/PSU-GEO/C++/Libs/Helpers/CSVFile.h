#pragma once

#include <string>
#include <vector>

using namespace std;

class CSVFile
{
private: 
	string _filename;
public:		
	vector < vector<string>> fileVector;	
	bool exists;
public:
	CSVFile(string filepath, string sep, bool load);	
	bool in(string match);
};

