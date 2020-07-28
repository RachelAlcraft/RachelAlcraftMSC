#pragma once
/*
This class replaces the information inside a formerly PDBFile because
a) it might come from a different file format
b) the pdb files have multiple versions of their structures determined by the occupancy
*/

#include <string>
#include <vector>
#include <map>
#include "AminoAcid.h"
#include "Atom.h"
#include "Chain.h"


class ProteinStructure
{
public://determining features of the structure
	string pdbCode;
	string occupant;


private:
	map<string, Chain*> _chains;

public:
	ProteinStructure(string, string);
	~ProteinStructure();		
	map<string, Chain*> getChains() { return _chains; }
	Chain* getChain(string chainId);
	map<int, Atom*> getAtoms(string pdbCode);
	void addChain(Chain* ch);
	void removeChain(string ch);
	void applyTransformation(GeoTransformations* trans);	
	string getSequence();
	void removeRepeatedChains();
	bool hasInsertions();
private:
	


};

