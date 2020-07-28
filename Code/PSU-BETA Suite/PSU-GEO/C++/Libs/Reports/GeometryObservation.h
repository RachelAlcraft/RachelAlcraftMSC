#pragma once
#include <string>
#include <vector>

using namespace std;


class GeometryObservation
{
	//PdbCode,Chain,AminoAcid,AminoNo,PdbAtoms,SecStruct,GeoType,ExperimentalMethod,GeoAtoms,Value
public:
	double value = 0;
	string pdbCode;
	string aminoCode;
	string aminoNo;	
	string pdbAtoms;
	string secStruc;
	string geoType; //ANGLE, BOND, ONEFOUR, IMPROPER, DIHEDRAL, INTER
	string geoAtoms; //N-C-O
	string allAAs; //Ala-Pro-Met
	
};

