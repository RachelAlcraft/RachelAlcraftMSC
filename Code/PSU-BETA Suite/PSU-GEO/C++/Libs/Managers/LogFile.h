#pragma once
/*###########################################################
Singleton class for logging
#############################################################
*/
#pragma warning(disable : 4996) //_CRT_SECURE_NO_WARNINGS
#include <time.h>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>
#include <codecvt>

using namespace std;

class LogFile
{
private:
	static LogFile* instance;
	LogFile();
	tm* _starttime;
	time_t _start;
	string _fileName;
	string _runId;
public:
	static LogFile* getInstance();
	bool setLogFile(string fileName, string path);
	void writeMessage(string msg);
	string runId();
private:
	bool CreateFolder(string path);	
};

