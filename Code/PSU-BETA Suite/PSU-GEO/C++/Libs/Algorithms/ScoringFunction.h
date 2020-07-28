#pragma once
#include <PDBFile.h>
#include <Atom.h>

/*
Currently uncertain what sort of scoring function this is destined to be
But I do need some certain infromation so may as well start gathering it
*/

class ScoringFunction
{
private:
	PDBFile* _pdb;
	vector<AtomBond> _bonds;
	vector<AtomAngle> _angles;
	vector<AtomTorsion> _torsions;


public:
	ScoringFunction(PDBFile* pdb);
	void getAtomInfo();
};

