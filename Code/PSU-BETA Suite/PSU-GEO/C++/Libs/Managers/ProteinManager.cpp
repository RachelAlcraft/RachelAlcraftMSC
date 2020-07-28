#include "ProteinManager.h"
#include <vector>
#include <fstream>
#include <sstream>
#include <map>
#include "PDBFile.h"
#include <LogFile.h>
#include <StringManip.h>
#include <NucleicAcid.h>


using namespace std;

ProteinManager* ProteinManager::instance = 0;

ProteinManager::ProteinManager()
{

}
ProteinManager::~ProteinManager() //responsible for pdbs
{
	for (map<string, PDBFile*>::iterator iter = _pdbfiles.begin(); iter != _pdbfiles.end(); ++iter)
	{
		delete iter->second;
	}
	_pdbfiles.clear();
}

void ProteinManager::deletePdbs()
{
	for (map<string, PDBFile*>::iterator iter = _pdbfiles.begin(); iter != _pdbfiles.end(); ++iter)
	{
		delete iter->second;
	}
	_pdbfiles.clear();
}

ProteinManager* ProteinManager::getInstance()
{
	if (!instance)
		instance = new ProteinManager();
	return instance;
}

void ProteinManager::createAminoAcidData(string filename)
{	
	//AMINO ACID GENERAL DATA//////////////////////////////////////////////
	//Load the amino acid general info, note the chi definitions are actually used to create chi angles	
	vector<string> file;
	ifstream myfile(filename);
	if (myfile.is_open())
	{
		string line = "";
		while (getline(myfile, line))
			file.push_back(line);
	}
	//Each vector starts with 3 letter code and then has a string of info, comma delim
	for (unsigned int i = 0; i < file.size(); ++i)
	{
		string line = file[i];
		int pos = line.find(",");
		if (pos > 0)
		{
			string aa = line.substr(0, pos);			
			if (aa.length() == 3)
				_aa_generaldata.insert(pair<string, string>(aa, line));//no error checking! It is fixed data. Should be correct!
		}
	}


	//GEOMETRIC VALUES//////////////////////////////////////////////

	//FORCE FIELD///////////////////////////////////////////////////

}

PDBFile* ProteinManager::getOrAddPDBFile(string pdbCode, string filename)
{
	map<string, PDBFile*>::iterator iter = _pdbfiles.find(pdbCode);
	if (iter == _pdbfiles.end())
	{
		PDBFile* pdb = new PDBFile(filename,pdbCode);
		_pdbfiles.insert(pair<string, PDBFile*>(pdbCode, pdb));
		return pdb;
	}
	else
	{
		return iter->second;
	}
}

vector<string> ProteinManager::getAminoData(string aminoCode)
{
	return StringManip::stringToVector(_aa_generaldata[aminoCode],",");//unvalidated. Whole system relies on data being good for now.
}

void ProteinManager::addAtom(string pdbCode, string occupant, string chainId, int aminoId, Atom* atm)
{
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	Chain* chain = ps->getChain(chainId);
	AminoAcid* aa = chain->getAminoAcid(aminoId);
	aa->add(atm);
}


bool ProteinManager::isAminoAcid(string code)
{
	return true;
}

bool ProteinManager::isNucleicAcid(string code)
{
	if (code.length() < 3)
		return true;
	else
		return false;
}

NucleicAcid* ProteinManager::getOrAddNucleicAcid(string pdbCode, string occupant, string chainId, int aminoId, string aminoCode, int& structure_id, int& nucleonum)
{
	try
	{
		stringstream id;
		id << pdbCode << chainId << aminoId;

		PDBFile* pdb = _pdbfiles[pdbCode];
		ProteinStructure* ps = pdb->getStructureVersion(occupant);
		Chain* chain = ps->getChain(chainId);
		if (chain)
		{
			NucleicAcid* na = chain->getNucleicAcid(aminoId);
			if (!na)
			{
				structure_id += 1;
				NucleicAcid* na = new NucleicAcid(aminoId);
				chain->addNucleicAcid(na);
				++nucleonum;
				return na;
			}
			else
			{
				return na;
			}
		}
		else
		{
			LogFile::getInstance()->writeMessage("Amino acid not found " + pdbCode);
			return nullptr;
		}
	}
	catch (...)
	{
		LogFile::getInstance()->writeMessage("Amino acid not found " + pdbCode);
		return nullptr;
	}

}

AminoAcid* ProteinManager::getOrAddAminoAcid(string pdbCode, string occupant, string chainId, int aminoId, string aminoCode, int& structure_id)
{
	try
	{
		stringstream id;
		id << pdbCode << chainId << aminoId;

		PDBFile* pdb = _pdbfiles[pdbCode];
		ProteinStructure* ps = pdb->getStructureVersion(occupant);
		Chain* chain = ps->getChain(chainId);
		
		if (aminoId > 0)
		{
			if (chain && aminoCode != "UNK")
			{
				AminoAcid* aa = chain->getAminoAcid(aminoId);
				if (!aa)
				{
					structure_id += 1;
					AminoAcid* aa = new AminoAcid(pdbCode, chainId, aminoId, structure_id, aminoCode);
					chain->addAminoAcid(aa);
					//++residuenum;
					return aa;
				}
				else
				{
					return aa;
				}
			}
			else
			{
				LogFile::getInstance()->writeMessage("Amino acid not found " + pdbCode + " " + aminoCode);
				return nullptr;
			}
		}
		else
		{
			//LogFile::getInstance()->writeMessage("Negative or 0 amino number " + pdbCode);
			return nullptr;
		}
	}
	catch (...)
	{
		LogFile::getInstance()->writeMessage("Amino acid not found " + pdbCode + " " + aminoCode);
		return nullptr;
	}
	
}
Chain* ProteinManager::getOrAddChain(string pdbCode, string occupant, string chainId)
{
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	if (!ps)
	{//if it is a new protein structure it wants to be a copy of the previous one
		pdb->addStructureVersion(occupant);
		ps = pdb->getStructureVersion(occupant);
	}
	Chain* chain = ps->getChain(chainId);
	if (!chain)
	{
		Chain* ch = new Chain(pdbCode, chainId);
		ps->addChain(ch);
		return ch;
	}
	else
	{
		return chain;
	}	
}
map<string, Chain*> ProteinManager::getChains(string pdbCode, string occupant)
{
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	return ps->getChains();
}
map<int, AminoAcid*> ProteinManager::getAminoAcids(string pdbCode, string occupant, string chainId)
{
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	Chain* chain = ps->getChain(chainId);
	return chain->getAminoAcids();

}

vector<Atom*>  ProteinManager::getCAlphas(string pdbCode, string occupant, string chainId, string atom)
{
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	Chain* chain = ps->getChain(chainId);
	return chain->getCAlphas(atom);	
}

vector<Atom*> ProteinManager::getCAlphas(string pdbCode, string occupant, string atom)
{
	vector<Atom*> calphas;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string,Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		vector<Atom*> cas = ch->getCAlphas(atom);
		for (unsigned int i = 0; i < cas.size(); ++i)
			calphas.push_back(cas[i]);
	}	
	return calphas;
}

vector<Atom*>  ProteinManager::getAtoms(string pdbCode, string occupant)
{
	vector<Atom*> vecatoms;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			map<string,Atom*> atoms = biter->second->getAtoms();
			for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)			
				vecatoms.push_back(citer->second);
		}
		
	}
	return vecatoms;	
}

map<int,Atom*>  ProteinManager::getAtomsMap(string pdbCode, string occupant)
{
	map<int,Atom*> mapatoms;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			map<string, Atom*> atoms = biter->second->getAtoms();
			for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)
			{
				if (citer->second)
					mapatoms.insert(pair<int, Atom*>(citer->second->atomId, citer->second));
			}
		}

	}
	return mapatoms;
}

vector<AtomBond>  ProteinManager::getAtomBonds(string pdbCode, string occupant)
{
	vector<AtomBond> vecatoms;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			vector<AtomBond> atoms = biter->second->getAtomBonds();
			for (unsigned int i = 0; i < atoms.size(); ++i)
				vecatoms.push_back(atoms[i]);
		}

	}
	return vecatoms;
}

vector<AtomAngle>  ProteinManager::getAtomAngles(string pdbCode, string occupant)
{
	vector<AtomAngle> vecatoms;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			vector<AtomAngle> atoms = biter->second->getAtomAngles();
			for (unsigned int i = 0; i < atoms.size(); ++i)
				vecatoms.push_back(atoms[i]);
		}

	}
	return vecatoms;
}
vector<AtomTorsion>  ProteinManager::getAtomTorsions(string pdbCode, string occupant)
{
	vector<AtomTorsion> vecatoms;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			vector<AtomTorsion> atoms = biter->second->getAtomTorsions();
			for (unsigned int i = 0; i < atoms.size(); ++i)
				vecatoms.push_back(atoms[i]);
		}

	}
	return vecatoms;
}

bool ProteinManager::hasOccupancy(string pdbCode, string occupant)
{
	bool hasOccupancy = false;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			map<string, Atom*> atoms = biter->second->getAtoms();
			for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)
			{
				double occ = citer->second->occupancy;
				if (occ != 1)
				{
					hasOccupancy = true;
				}				
			}
		}
	}	
	return hasOccupancy;
}

vector<string> ProteinManager::occupantList(string pdbCode)
{
	vector<string> occList;
	PDBFile* pdb = _pdbfiles[pdbCode];
	map <string, ProteinStructure*> pss = pdb->getStructureVersions();
	for (map<string, ProteinStructure*>::iterator aiter = pss.begin(); aiter != pss.end(); ++aiter)
	{
		ProteinStructure* ps = aiter->second;
		map<string, Chain*> chains = ps->getChains();
		for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
		{
			Chain* ch = iter->second;
			map<int, AminoAcid*> aminos = ch->getAminoAcids();
			for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
			{
				map<string, Atom*> atoms = biter->second->getAtoms();
				for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)
				{
					string occ = citer->second->occupant;
					if (std::find(occList.begin(), occList.end(), occ) == occList.end())
					{
						occList.push_back(occ);
					}
				}
			}
		}		
	}
	return occList;
}

double ProteinManager::maxBFactor(string pdbCode, string occupant)
{
	double maxbf = 0;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			map<string, Atom*> atoms = biter->second->getAtoms();
			for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)
			{
				double mbf = citer->second->bfactor;
				if (mbf > maxbf)
				{
					maxbf = mbf;
				}
			}
		}
	}
	return maxbf;
}


bool ProteinManager::hasHydrogens(string pdbCode, string occupant)
{
	bool hasHyd = false;
	PDBFile* pdb = _pdbfiles[pdbCode];
	ProteinStructure* ps = pdb->getStructureVersion(occupant);
	map<string, Chain*> chains = ps->getChains();
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* ch = iter->second;
		map<int, AminoAcid*> aminos = ch->getAminoAcids();
		for (map<int, AminoAcid*>::iterator biter = aminos.begin(); biter != aminos.end(); ++biter)
		{
			map<string, Atom*> atoms = biter->second->getAtoms();
			for (map<string, Atom*>::iterator citer = atoms.begin(); citer != atoms.end(); ++citer)
			{
				string ele = citer->second->elementName;
				if (ele == "H")
				{
					hasHyd = true;
				}

			}
		}
	}

	return hasHyd;
}

