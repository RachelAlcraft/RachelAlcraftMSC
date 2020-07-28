#pragma once

#include <vector>
#include <PDBFile.h>
#include <FASTAFile.h>
#include <string>
#include <sstream>
#include <Atom.h>

using namespace std;

class AtomPair
{
public:
	Atom* a1;
	Atom* a2;
	AtomPair(Atom* aa, Atom* ab)
	{
		a1 = aa;
		a2 = ab;
	}
};

class LeastSquares
{
public:
	PDBFile* PDB1;
	PDBFile* PDB2;
	FastaFile* Fasta;
	bool Alignment;

public:
	LeastSquares(PDBFile* pdb1, PDBFile* pdb2, bool align);
private:
	vector<AtomPair> _atomPairsAlignment;	
	stringstream reportStream;


public:
	void setupAtomPairs();
	double calculateRMSDLeastSquares();
	void applyRMSDLeastSquares();
	string report() { return  reportStream.str(); }
};

