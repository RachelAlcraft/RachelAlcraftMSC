#pragma once

#include <string>
#include <map>
#include <AminoAcid.h>
#include <NucleicAcid.h>

using namespace std;

class Chain
{
public:
	//Parent
	string pdbCode;
	string dataId;
	string chainId;

	//Children
	map<int, AminoAcid*> _aminos;
	map<int, NucleicAcid*> _nucleics;

public:
	Chain(string pdb_code, string chain_id);
	~Chain();
	AminoAcid* getAminoAcid(int aminoId);
	NucleicAcid* getNucleicAcid(int aminoId);
	map<int, AminoAcid*> getAminoAcids() { return _aminos; }
	vector<Atom*>  getCAlphas(string atom);
	void addAminoAcid(AminoAcid* aa);
	void addNucleicAcid(NucleicAcid* na);
	bool hasInsertions();
};

