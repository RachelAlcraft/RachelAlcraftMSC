#pragma once
/*###########################################################
Singleton class for controlling the input paramters for the run
#############################################################
*/
#include <string>
#include <map>

using namespace std;

class InputParams
{

private:
	static InputParams* instance;
	InputParams();
	string _fileName;	
	map<string, string> _params;

public:
	static InputParams* getInstance();
	void setInputFile(string fileName);	
	string getParam(string);
	
};

