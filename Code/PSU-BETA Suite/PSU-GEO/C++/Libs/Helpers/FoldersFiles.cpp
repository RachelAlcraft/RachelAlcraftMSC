#include "FoldersFiles.h"

#include <StringManip.h>
#include <Windows.h>



vector<string> FoldersFiles::getFilesWithinFolder(string folder)
{//https://stackoverflow.com/questions/612097/how-can-i-get-the-list-of-files-in-a-directory-using-c-or-c
	vector<string> names;
	string search_path = folder + "*.*";
	wstring wrpath = StringManip::utf8ToUtf16(search_path);
	LPCWSTR lpr = wrpath.c_str();
	WIN32_FIND_DATA fd;
	HANDLE hFind = ::FindFirstFile(lpr, &fd);
	if (hFind != INVALID_HANDLE_VALUE)
	{
		do {
			// read all (real) files in current folder
			// , delete '!' read other 2 default folder . and ..
			if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
			{
				wstring fs = fd.cFileName;
				string s = StringManip::ws2s(fs);
				names.push_back(s);
			}
		} while (::FindNextFile(hFind, &fd));
		::FindClose(hFind);
	}
	return names;
}