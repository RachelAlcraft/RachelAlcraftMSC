#include "AminoAcid.h"
#include "ProteinManager.h"
#include <StringManip.h>
#include <sstream>
#include <LogFile.h>

AminoAcid::AminoAcid(string pdb_code, string chain_id, int amino_id, int structure_id, string amino_Code)
{
	_torsion = nullptr;
	_sideTorsion = nullptr;
	_aaPrev = nullptr;
	_aaNext = nullptr;
	_atmCp = nullptr;
	_atmNpp = nullptr;
	_atmCApp = nullptr;

	aminoId = amino_id;	
	//structureAaId = structure_id;
	pdbCode = pdb_code;
	chainId = chain_id;
	aminoCode = amino_Code;
	vector<string> aa_general = ProteinManager::getInstance()->getAminoData(aminoCode);
	if (aa_general.size() > 1)
	{
		//general data setttings
		AminoCode = aa_general[0];
		AminoName = aa_general[1];
		AminoLetter = aa_general[2];
		Hydro = atof(aa_general[3].c_str());
		Hydropathy = aa_general[4];
		Volume = atof(aa_general[5].c_str());
		Donicity = aa_general[6];
		Chemical = aa_general[7];
		Physio = aa_general[8];
		Charge = atol(aa_general[9].c_str());
		Polar = aa_general[10] == "T" ? true : false;
		Formula = aa_general[11];
		AtomChain = aa_general[12];
		Chi1 = aa_general[13];
		Chi2 = aa_general[14];
		Chi3 = aa_general[15];
		Chi4 = aa_general[16];
		Chi5 = aa_general[17];
	}
	else
	{

	}
}

AminoAcid::~AminoAcid()
{
	delete _torsion;
	delete _sideTorsion;
	_torsion = nullptr;
	_sideTorsion = nullptr;
	_aaPrev = nullptr;
	_aaNext = nullptr;
	_atmCp = nullptr;
	_atmNpp = nullptr;
	_atmCApp = nullptr;
	
	for (map<string, Atom*>::iterator iter = _atoms.begin(); iter != _atoms.end(); ++iter)
	{
		//possibly atoms can live in multiple places due to occupancy...
		if (iter->second)
			delete iter->second;
	}
	_atoms.clear();
}

/*void AminoAcid::createBondsFromGeoDef(AminoAcid* aaP, AminoAcid* aaPP, GeoDataReport& gdr)
{

}*/

void AminoAcid::createBonds(AminoAcid* aaP, AminoAcid* aaPP)
{ //Bonds are formed in the order
	//C'-N-CA-C-N''-CA''
	_aaPrev = aaP;
	_aaNext = aaPP;

	//if we are at the beginning or end of a chain we don't do the backbone phi psi omega
	if (_aaPrev && _aaNext)
	{
		//Set all atom references
		_atmCp = _aaPrev->_atoms["C"];
		_atmCApp = _aaNext->_atoms["CA"];
		_atmNpp = _aaNext->_atoms["N"];

		if (!_atmCp || !_atmCApp || !_atmNpp)
		{
			//raise an error here
			stringstream ss;
			ss << "Some missing atoms on either side :AA=" << aminoCode << " Id=" << aminoId;
			//LogFile::getInstance()->writeMessage(ss.str());
		}

		vector<Atom*> backbones = atomsFromString("CP-N-CA-C-NPP-CAPP");
		_torsion = new BackboneTorsion(aminoCode, aminoId, backbones);
	}
	else
	{		
		//stringstream ss;
		//ss << "No backbone - chain end :AA=" << aminoCode << " Id=" << aminoId;
		//LogFile::getInstance()->writeMessage(ss.str());
	}

	vector<vector<Atom*>> sidechains;
	if (Chi1 != "None")
		sidechains.push_back(atomsFromString(Chi1));	
	if (Chi2 != "None")	
		sidechains.push_back(atomsFromString(Chi2));	
	if (Chi3 != "None")
		sidechains.push_back(atomsFromString(Chi3));			
	if (Chi4 != "None")
		sidechains.push_back(atomsFromString(Chi4));			
	if (Chi5 != "None")	
		sidechains.push_back(atomsFromString(Chi5));
	
	_sideTorsion = new SidechainTorsion(aminoCode, aminoId, sidechains);

	
}

void AminoAcid::add(Atom* atom)
{
	_atoms.insert(pair<string, Atom*>(atom->elementName, atom));
}

vector<Atom*> AminoAcid::atomsFromString(string atomstring)
{//For beginning and end of chains we return nothing by checking the pointers to the previous and next
	vector<string> stratoms = StringManip::stringToVector(atomstring, "-");
	vector<Atom*> vecatoms;
	bool bCompleteSet = true;	
	for (unsigned int i = 0; i < stratoms.size(); ++i)
	{
		Atom* atm = nullptr;
		string stratom = stratoms[i];
		string strtype = stratom;
		int npos = stratom.find("N");
		int capos = stratom.find("CA");		
		int opos = stratom.find("O");
		int cbpos = stratom.find("CB");
		int cpos = stratom.find("C");
		if (npos == 0)//identify the type if an NPP2 or CAP4 for example
			strtype = "N";
		else if (capos == 0)
			strtype = "CA";
		else if (opos == 0)
			strtype = "O";
		else if (cbpos == 0)
			strtype = "CB";
		else if (cpos == 0)//C last as there is CA and CB
			strtype = "C";
		int howManyPre = 0;
		int howManyNext = 0;

		int nextpos = stratom.find("PP");
		int prepos = stratom.find("P");
		bool isNext = nextpos > 0 ? true : false;
		bool isPre = false;
		if (!isNext) // PP trumps P in the find
			isPre = prepos > 0 ? true : false;

		if (isPre && _aaPrev)
		{
			if (stratom.find("P6") != string::npos)
			{
				if (_aaPrev->_aaPrev)
				{
					if (_aaPrev->_aaPrev->_aaPrev)
					{
						if (_aaPrev->_aaPrev->_aaPrev->_aaPrev)
						{
							if (_aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev)
							{
								if (_aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev)
								{
									atm = _aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev->_atoms[strtype];
								}
							}
						}
					}
				}
			}
			else if (stratom.find("P5") != string::npos)
			{
				if (_aaPrev->_aaPrev)
				{
					if (_aaPrev->_aaPrev->_aaPrev)
					{
						if (_aaPrev->_aaPrev->_aaPrev->_aaPrev)
						{
							if (_aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev)
							{																
								atm = _aaPrev->_aaPrev->_aaPrev->_aaPrev->_aaPrev->_atoms[strtype];								
							}
						}
					}
				}
			}
			else if (stratom.find("P4") != string::npos)
			{
				if (_aaPrev->_aaPrev)
				{
					if (_aaPrev->_aaPrev->_aaPrev)
					{
						if (_aaPrev->_aaPrev->_aaPrev->_aaPrev)
						{														
							atm = _aaPrev->_aaPrev->_aaPrev->_aaPrev->_atoms[strtype];							
						}
					}
				}
			}
			else if (stratom.find("P3") != string::npos)
			{
				if (_aaPrev->_aaPrev)
				{
					if (_aaPrev->_aaPrev->_aaPrev)
					{												
						atm = _aaPrev->_aaPrev->_aaPrev->_atoms[strtype];						
					}
				}
			}
			else if (stratom.find("P2") != string::npos)
			{
				if (_aaPrev->_aaPrev)
				{										
					atm = _aaPrev->_aaPrev->_atoms[strtype];					
				}
			}
			else
			{
				atm = _aaPrev->_atoms[strtype];
			}												
		}
		else if (isNext && _aaNext)
		{
			if (stratom.find("PP6") != string::npos)
			{
				if (_aaNext->_aaNext)
				{
					if (_aaNext->_aaNext->_aaNext)
					{
						if (_aaNext->_aaNext->_aaNext->_aaNext)
						{
							if (_aaNext->_aaNext->_aaNext->_aaNext->_aaNext)
							{
								if (_aaNext->_aaNext->_aaNext->_aaNext->_aaNext->_aaNext)
								{
									atm = _aaNext->_aaNext->_aaNext->_aaNext->_aaNext->_aaNext->_atoms[strtype];
								}
							}
						}
					}
				}
			}
			else if (stratom.find("PP5") != string::npos)
			{
				if (_aaNext->_aaNext)
				{
					if (_aaNext->_aaNext->_aaNext)
					{
						if (_aaNext->_aaNext->_aaNext->_aaNext)
						{
							if (_aaNext->_aaNext->_aaNext->_aaNext->_aaNext)
							{
								atm = _aaNext->_aaNext->_aaNext->_aaNext->_aaNext->_atoms[strtype];
							}
						}
					}
				}
			}
			else if (stratom.find("PP4") != string::npos)
			{
				if (_aaNext->_aaNext)
				{
					if (_aaNext->_aaNext->_aaNext)
					{
						if (_aaNext->_aaNext->_aaNext->_aaNext)
						{
							atm = _aaNext->_aaNext->_aaNext->_aaNext->_atoms[strtype];
						}
					}
				}
			}
			else if (stratom.find("PP3") != string::npos)
			{
				if (_aaNext->_aaNext)
				{
					if (_aaNext->_aaNext->_aaNext)
					{
						atm = _aaNext->_aaNext->_aaNext->_atoms[strtype];
					}
				}
			}
			else if (stratom.find("PP2") != string::npos)
			{
				if (_aaNext->_aaNext)
				{
					atm = _aaNext->_aaNext->_atoms[strtype];
				}
			}
			else
			{
				atm = _aaNext->_atoms[strtype];
			}
		}
		else
		{
			atm = _atoms[stratom];
		}
		if (atm)
			vecatoms.push_back(atm);
		else
			bCompleteSet = false;
		
	}
	if (bCompleteSet)
		return vecatoms;
	else
		return vector<Atom*>();
}

string AminoAcid::getSS()
{
	/*
	A right-handed helix (inc. aR and 3-10 )
	B ideal b-strand, parallel and anti-parallel b-sheet 
	P named after the polyproline helix, but is also a
	common b-strand conformation )
	L left-handed ?-helix 
	G left-handed glycine ‘helix’ 
	E extended conformation of glycine 
	From MSc Bioinformatics Birkbeck, 2020 Structural Bioinformatics module
	*/
	//Find the secondary structure on the ramachandran plot based on simple rules
	string ss = "U";
	if (_torsion)
	{
		double phi = _torsion->getPhi();
		double psi = _torsion->getPsi();

		if (phi <= -90 && psi >= 60)
			ss = "B";
		else if (phi < -20 && phi >= -90 && psi >= 60)
			ss = "P";
		else if (phi <= 0 && psi >= -90 && psi <= 60)
			ss = "A";
		else if (phi <= -90 && psi >= -180 && psi <= -145)
			ss = "B";
		else if (phi <= -50 && phi >= -90 && psi >= -180 && psi <= -150)
			ss = "P";
		else if (phi <= 180 && phi >= 60 && psi >= 120 && psi <= 180)
			ss = "E";
		else if (phi <= 70 && phi >= 30 && psi >= 10 && psi <= 70)
			ss = "L";
		else if (phi <= 150 && phi >= 60 && psi >= -40 && psi <= 60)
			ss = "G";
		else if (phi <= 180 && phi >= 30 && psi >= -180 && psi <= -90)
			ss = "G";
		else
			ss = "U";
	}
	return ss;
}

void AminoAcid::createScoringAtoms()
{
	//We create bonds and angles to the next aa not the previous
	string bondstring = AtomChain; //Not technically the atoms that are bonded, but it will do for now for the geometry
	vector<Atom*> aaatoms = atomsFromString(AtomChain);
	Atom* last = nullptr;
	string ss = getSS();
	// BONDS #########################
	for (int i = 0; i < (int)(aaatoms.size()) - 1; ++i)
	{
		Atom* a1 = aaatoms[i];
		Atom* a2 = aaatoms[i + 1];		
		_bonds.push_back(AtomBond(this->AminoCode,this->chainId,this->aminoId,ss,a1, a2,"","", ""));
		last = a2;
	}
	//Then we need the bond that goes to the next atom (unless it is the end)
	//TODO although currently I don't think this is being called if it is either the first or last
	if (_atmNpp && last)
	{		
		_bonds.push_back(AtomBond(this->AminoCode, this->chainId, this->aminoId, ss, last, _atmNpp, "","", ""));
	}
	// ANGLES #########################
	Atom* last1 = nullptr;
	Atom* last2 = nullptr;
	for (int i = 0; i < (int)(aaatoms.size()) - 2; ++i)
	{
		Atom* a1 = aaatoms[i];
		Atom* a2 = aaatoms[i + 1];
		Atom* a3 = aaatoms[i + 2];		
		_angles.push_back(AtomAngle(this->AminoCode, this->chainId, this->aminoId, ss, a1, a2, a3, "","", ""));
		last1 = a2;
		last2 = a3;
	}
	if (_atmNpp && _atmCApp && last1 && last2)
	{		
		_angles.push_back(AtomAngle(this->AminoCode, this->chainId, this->aminoId, ss, last1, last2, _atmNpp, "","", ""));
		_angles.push_back(AtomAngle(this->AminoCode, this->chainId, this->aminoId, ss, last2, _atmNpp, _atmCApp, "","", ""));
	}
	// TORSIONS ######################### //This is entirely made up sets of angles but consistent for now anyway
	last1 = nullptr;
	last2 = nullptr;
	Atom* last3 = nullptr;
	for (int i = 0; i < (int)(aaatoms.size()) - 3; ++i)
	{
		Atom* a1 = aaatoms[i];
		Atom* a2 = aaatoms[i + 1];
		Atom* a3 = aaatoms[i + 2];
		Atom* a4 = aaatoms[i + 3];		
		_torsions.push_back(AtomTorsion(this->AminoCode, this->chainId, this->aminoId, ss, a1, a2, a3, a4, "","",""));
		last1 = a2;
		last2 = a3;
		last3 = a4;
	}
	if (_atmNpp && _atmCApp && last1 && last2&& last3)
	{		
		_torsions.push_back(AtomTorsion(this->AminoCode, this->chainId, this->aminoId, ss, last1, last2, last3, _atmNpp, "","", ""));
		_torsions.push_back(AtomTorsion(this->AminoCode, this->chainId, this->aminoId, ss, last2, last3, _atmNpp, _atmCApp, "","", ""));
	}
}

bool AminoAcid::hasInsertions()
{
	bool bInsertions = false;
	for (map<string, Atom*>::iterator iter = _atoms.begin(); iter != _atoms.end(); ++iter)
	{		
		if (iter->second)
			bInsertions = bInsertions || iter->second->bInsertion;
	}
	return bInsertions;
}

//Geometric definitions features
vector<AtomGeo*> AminoAcid::getAtomDistance(vector<pair<string, string>> atoms, string geotype)
{
	vector<AtomGeo*> vab;
	for (unsigned int i = 0; i < atoms.size(); ++i)
	{
		string atomsdef = atoms[i].first;
		string alias = atoms[i].second;
		vector<Atom*> vatoms = atomsFromString(atomsdef);
		if (vatoms.size() == 2)
		{
			Atom* a1 = vatoms[0];
			Atom* a2 = vatoms[1];
			vab.push_back(new AtomBond(this->AminoCode, this->chainId, this->aminoId, getSS(), a1, a2, atomsdef, alias,geotype));

		}
		else
		{
			int hpos = atomsdef.find("H");// don't report hydrogens or there will be too many
			int ppos = atomsdef.find("P");// don't report previous and last again we will have too many messages for chain ends
			if (hpos == -1 && ppos == -1)
			{
				stringstream ss;
				ss << "-----Some missing bond atoms: Pdb=" << pdbCode << " AA=" << aminoCode << " Id=" << aminoId << " Atoms=" << atomsdef;
				//LogFile::getInstance()->writeMessage(ss.str());
			}
		}
	}
	return vab;
}

vector<AtomGeo*> AminoAcid::getAtomAngles(vector<pair<string, string>> atoms, string geotype)
{
	vector<AtomGeo*> vab;
	for (unsigned int i = 0; i < atoms.size(); ++i)
	{
		string atomsdef = atoms[i].first;
		string alias = atoms[i].second;

		vector<Atom*> vatoms = atomsFromString(atomsdef);
		if (vatoms.size() == 3)
		{
			Atom* a1 = vatoms[0];
			Atom* a2 = vatoms[1];
			Atom* a3 = vatoms[2];
			vab.push_back(new AtomAngle(this->AminoCode, this->chainId, this->aminoId, getSS(), a1, a2,a3,atomsdef,alias, geotype));
		}
		else
		{
			int hpos = atomsdef.find("H");// don't report hydrogens or there will be too many
			int ppos = atomsdef.find("P");// don't report previous and last again we will have too many messages for chain ends
			if (hpos == -1 && ppos == -1)
			{
				stringstream ss;
				ss << "-----Some missing angle atoms: Pdb=" << pdbCode << " AA=" << aminoCode << " Id=" << aminoId << " Atoms=" << atomsdef;
				//LogFile::getInstance()->writeMessage(ss.str());
			}
		}
	}
	return vab;
}
vector<AtomGeo*> AminoAcid::getAtomDihedrals(vector<pair<string, string>> atoms, string geotype)
{
	vector<AtomGeo*> vab;
	for (unsigned int i = 0; i < atoms.size(); ++i)
	{
		string atomsdef = atoms[i].first;
		string alias = atoms[i].second;

		vector<Atom*> vatoms = atomsFromString(atomsdef);
		if (vatoms.size() == 4)
		{
			Atom* a1 = vatoms[0];
			Atom* a2 = vatoms[1];
			Atom* a3 = vatoms[2];
			Atom* a4 = vatoms[3];
			vab.push_back(new AtomTorsion(this->AminoCode, this->chainId, this->aminoId, getSS(), a1, a2, a3,a4,atomsdef,alias, geotype));
		}
		else
		{
			int hpos = atomsdef.find("H");// don't report hydrogens or there will be too many
			int ppos = atomsdef.find("P");// don't report previous and last again we will have too many messages for chain ends
			if (hpos == -1 && ppos == -1)
			{
				stringstream ss;
				ss << "-----Some missing dihedral atoms: Pdb=" << pdbCode << " AA=" << aminoCode << " Id=" << aminoId << " Atoms=" << atomsdef;
				//LogFile::getInstance()->writeMessage(ss.str());
			}
		}
	}
	return vab;
}

