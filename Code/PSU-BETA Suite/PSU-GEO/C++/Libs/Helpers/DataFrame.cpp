#include "DataFrame.h"
#include <sstream>
#include <fstream>

using namespace std;

DataFrame::DataFrame(string filepath)
{
	_filename = filepath;
}

void DataFrame::print()
{
	stringstream ss;
	for (unsigned int i = 0; i < headerVector.size(); ++i)
	{
		if (i > 0)
			ss << ",";
		ss << headerVector[i];
	}

	for (unsigned int i = 0; i < fileVector.size(); ++i)
	{
		vector<string> row = fileVector[i];
		ss << "\n";
		for (unsigned int j = 0; j < row.size(); ++j)
		{
			if (j > 0)
				ss << ",";
			ss << row[j];
		}		
	}

	ofstream outfile(_filename);
	if (outfile.is_open())
	{
		outfile << ss.str();
	}
}

bool DataFrame::flush()
{
	stringstream ss;
	for (unsigned int i = 0; i < headerVector.size(); ++i)
	{
		if (i > 0)
			ss << ",";
		ss << headerVector[i];
	}

	for (unsigned int i = 0; i < fileVector.size(); ++i)
	{
		vector<string> row = fileVector[i];
		ss << "\n";
		for (unsigned int j = 0; j < row.size(); ++j)
		{
			if (j > 0)
				ss << ",";
			ss << row[j];
		}
	}

	ofstream outfile(_filename, ios_base::app );
	if (outfile.is_open())
	{
		outfile << ss.str();		
		outfile.close();		
		// And now clear the vectors out
		headerVector.clear();
		fileVector.clear();
		return true;		
	}
	else
	{
		return false;
	}		
}
