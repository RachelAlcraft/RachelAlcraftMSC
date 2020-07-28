#include "Chain.h"
#include <NucleicAcid.h>

Chain::Chain(string pdb_code,string chain_id)
{
	pdbCode = pdb_code;
	chainId = chain_id;
	dataId = pdbCode;
}

Chain::~Chain() //responsible for amino acids
{
	for (map<int, AminoAcid*>::iterator iter = _aminos.begin(); iter != _aminos.end(); ++iter)
	{
		delete iter->second;
	}
	_aminos.clear();
}

AminoAcid* Chain::getAminoAcid(int aminoId)
{
	map<int,AminoAcid*>::iterator iter = _aminos.find(aminoId);
	if (iter == _aminos.end())	
		return nullptr;
	else	
		return iter->second;		
}

bool Chain::hasInsertions()
{
	bool bInsertions = false;
	for (map<int, AminoAcid*>::iterator iter = _aminos.begin(); iter != _aminos.end(); ++iter)
	{
		AminoAcid *aa = iter->second;
		bInsertions = bInsertions || aa->hasInsertions();
	}
	return bInsertions;
}

NucleicAcid* Chain::getNucleicAcid(int nucleicId)
{
	map<int, NucleicAcid*>::iterator iter = _nucleics.find(nucleicId);
	if (iter == _nucleics.end())
		return nullptr;
	else
		return iter->second;
}

vector<Atom*> Chain::getCAlphas(string atom)
{
	vector<Atom*> calphas;
	for (map<int, AminoAcid*>::iterator iter = _aminos.begin(); iter != _aminos.end(); ++iter)
	{
		Atom* calpha = iter->second->getCAlpha(atom);
		if (calpha)
			calphas.push_back(calpha);
	}
	return calphas;
}

void Chain::addAminoAcid(AminoAcid* aa)
{
	map<int, AminoAcid*>::iterator iter = _aminos.find(aa->aminoId);
	if (iter == _aminos.end())
		_aminos.insert(pair<int, AminoAcid*>(aa->aminoId,aa));

}

void Chain::addNucleicAcid(NucleicAcid* na)
{
	map<int, NucleicAcid*>::iterator iter = _nucleics.find(na->nucleicId);
	if (iter == _nucleics.end())
		_nucleics.insert(pair<int, NucleicAcid*>(na->nucleicId, na));

}
