#include "CSVFile.h"
#include <fstream>
#include <StringManip.h>

CSVFile::CSVFile(string filepath, string sep, bool load)
{
	_filename = filepath;
	exists = false;

	ifstream myfile(_filename);
	if (myfile.is_open())
	{
		exists = true;
		if (load)
		{
			string line = "";
			while (getline(myfile, line))
			{
				//decide to delete some data I am not handling TODO!
				vector<string> row = StringManip::stringToVector(line, sep);
				fileVector.push_back(row);
			}
		}
		myfile.close();
	}
	else
	{
		exists = false;
	}
}

bool CSVFile::in(string match)
{
	bool isIn = false;
	for (unsigned int i = 0; i < fileVector.size(); ++i)
	{
		for (unsigned int j = 0; j < fileVector[i].size(); ++j)
		{
			int pos = fileVector[i][j].find(match);
			if (pos >= 0)
				isIn = true;

		}
	}
	return isIn;
}


