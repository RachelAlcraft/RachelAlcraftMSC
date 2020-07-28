#pragma once
/*
I should try to put all my windows specific files and folders operations in here
*/

#include <vector>
#include <string>


using namespace std;


class FoldersFiles
{
public:
	static vector<string> getFilesWithinFolder(string folder);
	static void setWorkingPathToExe();
};
