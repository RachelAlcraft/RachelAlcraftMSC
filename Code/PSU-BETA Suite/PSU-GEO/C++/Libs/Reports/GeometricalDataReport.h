#pragma once
#include <PDBFile.h>
#include <vector>

using namespace std;

class GeometricalDataReport
{
private:
	/*
	the file is of the format
	-------------------------------
	AminoAcid, GeoType, Atoms
	#Previousand next atoms, ,
	*,BOND,CP-N
	ILE,ONEFOUR,CD1-CG2
	-------------------------------
	Where a # means ignore, and a * means all amino acids
	*/
	vector < vector<string>> geoDefinitions;
		
public:
	GeometricalDataReport(vector < vector<string>> fileVector) { geoDefinitions = fileVector; }
	void printReport(PDBFile* pdb, string geodir, bool core, bool extra, bool atoms);
private:
	//void printOneReport(PDBFile* pdb, string occupant, string filename1);// , string filename2);
	void printOneReportWithGeoDef(PDBFile* pdb, string occupant, string fileName_geo);
	void printAtomsForGeoDef(PDBFile* pdb, string occupant, string fileName_atoms);
	void printCoreReportWithGeoDef(PDBFile* pdb, string occupant, string fileName_geo);

	vector<pair<string,string>> getGeoDefinitions(string aminoCode, string geoType);
	vector<string> getReportString(AtomGeo* ab, PDBFile* pdb, string occupant);
	string quickRound(double val);
	string quickInt(int val);
};

