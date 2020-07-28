#pragma once
#include <string>
#include <vector>

using namespace std;

class GeometricalAggregationReport
{
public:
	void printReport(string datadir);
	void printReport(vector<string> datafiles, string outdir, string aa);
private:
	//vector<string> getFilesWithinFolder(string folder);
};

