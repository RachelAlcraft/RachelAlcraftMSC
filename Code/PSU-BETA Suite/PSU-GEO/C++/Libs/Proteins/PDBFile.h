#pragma once

#include <string>
#include <vector>
#include <map>
#include "AminoAcid.h"
//#include <GeoTransformation.h>
//#include "Bond.h"
#include "Atom.h"
#include "Chain.h"
#include <ProteinStructure.h>


class PDBFile
{
private:
	string _filename;
	vector<string> _file; //The original file is saved so we can print it back out
public:
	string pdbCode;
	string experimentalMethod;
	//int residues;
	int nucleotides;
	string institution;
	string software;
	string date;
	string proteinclass;
	string rvalue;
	string rfree;	
	string resolution;
	string inComplex;
	bool nullModel;
//3 stages of initiation
	bool loadedText;
	bool loadedAminos;
	bool loadedBonds;
	bool loadedTorsions;

private:
	//map<string, Chain*> _chains;
	map<string, ProteinStructure*> _proteinVersions;
	bool idChains = false;
	bool breaks = false;
	bool insertions = false;
	bool negAminos = false;
	bool NCS = false;

public:
	PDBFile(string,string);
	~PDBFile();
	string getFileString();	
	void addLinks();
	ProteinStructure* getStructureVersion(string occupant);
	void addStructureVersion(string occupant);
	void removeStructureVersion(string occupant);
	map<string, ProteinStructure*> getStructureVersions() { return _proteinVersions; }
	bool areChainsIdentical();
	//map<string, Chain*> getChains() { return _chains; }
	//Chain* getChain(string chainId);
	//map<int, Atom*> getAtoms(string pdbCode);
	//void addChain(Chain* ch);
	void structureInfo();
	void loadData();
	void loadAtoms();
	void loadBonds();
	void loadTorsions();
	//void applyTransformation(GeoTransformations* trans);
	void printShiftedFile(string);
	vector<string> getSequence();
	string maxChain();
	void removeRepeatedChains();
	bool identicalChains() { return idChains; }
	bool hasBreaks() { return breaks; }
	bool hasInsertions();
	bool hasNegativeAminos() { return negAminos; }
	bool hasNCS() { return NCS; }
	

	


private:
	void createFileVector();
	void prepareStructureVersions();
	void areBreaks();
	void keepOnlyChainA();
	
	

};

