#include "InputParams.h"
#include "LogFile.h"
#include <fstream>
#include <sstream>
#include <vector>
#include "Windows.h"

InputParams* InputParams::instance = 0;

InputParams::InputParams()
{
	_fileName = "";
}

InputParams* InputParams::getInstance()
{
	if (!instance)
		instance = new InputParams();
	return instance;
}

void InputParams::setInputFile(string fileName)
{	
	//Get the input file from the same place as the exe
	char path[MAX_PATH] = "";
	GetModuleFileNameA(NULL, path, MAX_PATH);
	string strpath(path);
	int pos = strpath.find_last_of('\\');
	string inputPath = strpath.substr(0, pos + 1);
	_fileName = inputPath + fileName;

	vector<string> file;
	ifstream myfile(_fileName);
	if (myfile.is_open())
	{
		string line = "";
		while (getline(myfile, line))
			file.push_back(line);
	}
	for (unsigned int i = 0; i < file.size(); ++i)
	{
		string ln = file[i];
		stringstream ssln;
		ssln << ln;
		if (ln.length() > 1 && ln[0]!='#' && ln.find("=")>0)//comments are # and line must have something in
		{
			vector<string> line;
			string para;
			while (getline(ssln, para, '='))			
				line.push_back(para);
			if (line.size() == 2)
			{
				string param = line[0];
				string val = line[1];
				map<string, string>::iterator iter = _params.find(param);
				if (iter == _params.end())
					_params.insert(pair<string,string>(param,val));
				else
					LogFile::getInstance()->writeMessage("Param error, repeated " + param);

			}
		}		
	}
}

string InputParams::getParam(string param)
{
	map<string, string>::iterator iter = _params.find(param);
	if (iter != _params.end())
		return iter->second;
	else
		return "";

}

