#include "ProteinStructure.h"
#include <ProteinManager.h>


ProteinStructure::ProteinStructure(string pdb_code, string occupant_id)
{
	pdbCode = pdb_code;
	occupant = occupant_id;	
}

ProteinStructure::~ProteinStructure()
{
	map<int, Atom*> atoms = getAtoms(pdbCode);
			
	for (map<string, Chain*>::iterator iter = _chains.begin(); iter != _chains.end(); ++iter)
	{
		Chain* chain = iter->second;
		delete chain;
	}
	//a check that we did delete everything
	for (map<int, Atom*>::iterator iter = atoms.begin(); iter != atoms.end(); ++iter)
		delete iter->second;
}

Chain* ProteinStructure::getChain(string chainId)
{
	map<string, Chain*>::iterator iter = _chains.find(chainId);
	if (iter == _chains.end())
		return nullptr;
	else
		return iter->second;
}

map<int, Atom*> ProteinStructure::getAtoms(string pdbCode)
{
	map<int, Atom*> atoms;
	for (map<string, Chain*>::iterator iter = _chains.begin(); iter != _chains.end(); ++iter)
	{
		Chain* ch = iter->second;

	}

	return atoms;
}

void ProteinStructure::addChain(Chain* ch)
{
	map<string, Chain*>::iterator iter = _chains.find(ch->chainId);
	if (iter == _chains.end())
		_chains.insert(pair<string, Chain*>(ch->chainId, ch));
}

bool ProteinStructure::hasInsertions()
{
	bool bInsertions = false;
	for (map<string, Chain*>::iterator iter = _chains.begin(); iter != _chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		bInsertions = bInsertions || ch->hasInsertions();
	}
	return bInsertions;
}

void ProteinStructure::removeChain(string chL)
{
	map<string, Chain*> copyCh;
	
	for (map<string, Chain*>::iterator iter = _chains.begin(); iter != _chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		if (chL != iter->second->chainId)
			copyCh.insert(pair<string, Chain*>(ch->chainId, ch));
	}
	_chains = copyCh;
}

void ProteinStructure::applyTransformation(GeoTransformations* trans)
{
	vector<Atom*> atoms = ProteinManager::getInstance()->getAtoms(pdbCode,occupant);
	for (unsigned int i = 0; i < atoms.size(); ++i)
	{
		if (atoms[i])
			atoms[i]->applyTransformation(trans);
	}
}

string ProteinStructure::getSequence() 
{
	string seq = "";
	map<string, Chain*> chains = ProteinManager::getInstance()->getChains(pdbCode,occupant);
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* chain = iter->second;
		map<int, AminoAcid*> aminos = ProteinManager::getInstance()->getAminoAcids(pdbCode, occupant, chain->chainId);
		for (map<int, AminoAcid*>::iterator iteraa = aminos.begin(); iteraa != aminos.end(); ++iteraa)
		{
			seq += iteraa->second->AminoLetter;
		}
	}
	return seq;
}

void ProteinStructure::removeRepeatedChains()
{	
	map<string, Chain*>::iterator iter = _chains.begin();
	string letter = iter->first;
	Chain* ch = iter->second;
	++iter;
	for (; iter != _chains.end(); ++iter)	
		delete iter->second;
	_chains.clear();
	_chains.insert(pair<string, Chain*>(letter, ch));
}