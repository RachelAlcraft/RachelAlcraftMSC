#pragma once

#include <string>
#include <RMSD.h>
#include <LeastSquares.h>


using namespace std;


class RMSDReport
{
public:
	void printReport(RMSD* rmsd, string fileName, bool optimised, string fileroot);
	void printLeastSquaresReport(LeastSquares* ls, string fileName, string fileroot);
};

