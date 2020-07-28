#pragma once

#include <PDBFile.h>
#include <string>

using namespace std;

class RamaReport
{
public:
	void printReport(PDBFile* pdb,string occupant, string filename);
private:
	//string getSS(double phi, double psi);
};

