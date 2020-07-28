#pragma once

#include <string>
#include <vector>

using namespace std;

class StringManip
{
public:
	static string trim(string string_to_trim);
	static string removeChar(string string_to_trim, string char_remove, string replace);
	static vector<string> stringToVector(string input, string delim);
	static wstring utf8ToUtf16(const std::string& utf8Str);
	static string ws2s(const std::wstring& wstr);
	static string quickRound(double val);
	static string quickInt(int val);
};

