#include "CAlphaReport.h"
#include <LogFile.h>
#include <ProteinManager.h>

void CAlphaReport::printReport(PDBFile* pdb, string occupant, string chain1, string chain2, string contactA, string contactB, string fileName, double max_distance)
{//produce data frame report for R reporting
	bool bSomeData = false;
	LogFile::getInstance()->writeMessage("Starting C Aplpha distance map");
	if (chain1 != "" && chain2 != "")
	{
		printSingleChainReport(pdb, occupant, chain1, chain2, fileName,contactA, contactB);
	}
	else
	{
		stringstream report;
		//stringstream report_gnuX;
		//stringstream report_gnuY;
		report << getHeader() << "\n";
		map<string, Chain*> chains = ProteinManager::getInstance()->getChains(pdb->pdbCode, occupant);
		int lastResiduesA = 0;
		for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
		{
			Chain* chain = iter->second;
			string chainid = iter->first;
			stringstream ss;
			ss << "--- Distances for: chain " << chainid;
			LogFile::getInstance()->writeMessage(ss.str());

			map<int, AminoAcid*> aminos = ProteinManager::getInstance()->getAminoAcids(pdb->pdbCode, occupant,chainid);
			
			vector<Atom*> contactsA = ProteinManager::getInstance()->getCAlphas(pdb->pdbCode, occupant,chainid, contactA);
	
			for (unsigned int i = 0; i < contactsA.size(); ++i)
			{				
				//for (map<string, Chain*>::iterator iterb = iter/* don't double up, start from where we are*/; iterb != chains.end(); ++iterb)
				int lastResiduesB = 0;
				for (map<string, Chain*>::iterator iterb = chains.begin(); iterb != chains.end(); ++iterb)
				{
					Chain* chainb = iterb->second;
					vector<Atom*> atomsb = chainb->getCAlphas(contactB);
					map<int, AminoAcid*> aminosb = ProteinManager::getInstance()->getAminoAcids(pdb->pdbCode, "A",chainb->chainId);
					unsigned int start = 0;
					//bool chainself = false;
					/*if (iterb == iter)
					{
						start = i;
						chainself = true;
					}*/
					for (unsigned int j = start; j < atomsb.size(); ++j)
					{
						Atom* a = contactsA[i];
						AminoAcid* aa = aminos[a->aminoId];
						Atom* b = atomsb[j];
						AminoAcid* ab = aminosb[b->aminoId];
						double distance = a->atomicDistance(b,false);
						//check it is not itself or within 2 as that is trivial and a waste of database space
						int aid = aa->aminoId + lastResiduesA;
						int bid = ab->aminoId + lastResiduesB;
						if (abs(aid - bid) > 1)
						{
							if (distance < max_distance) 
							{							
								//stringstream ss;
								//ss << "Distances for: chain " << chain->chainId << ":" << a->atomId << ":" << a->aminoId << ":" << aa->aminoCode;
								//LogFile::getInstance()->writeMessage(ss.str());
							
								bSomeData = true;
								report << getRow(aa, a, ab, b, distance, false, lastResiduesA, lastResiduesB, contactA + "-" + contactB) << "\n";
							}
							//if (!(chainself & (i == j)))//and reverse to halve the time														
							//{
							//	report << getRow(ab, b, aa, a, distance, false, lastResiduesA, lastResiduesB, contactA + "-" + contactB) << "\n";
								//report_gnuX << ;
							//}

						}
					}
					lastResiduesB += aminosb.size();
				}
			}
			lastResiduesA += aminos.size();
		}
		if (bSomeData)
		{
			ofstream outfile(fileName);
			if (outfile.is_open())
			{
				outfile << report.str();
			}
		}
	}
}

void CAlphaReport::printSingleChainReport(PDBFile* pdb, string occupant,string chain1, string chain2, string fileName, string atomA, string atomB)
{//produce data frame report for R reporting

	stringstream report;
	report << getHeader() << "\n";
	Chain* pchain1 = ProteinManager::getInstance()->getOrAddChain(pdb->pdbCode,occupant,chain1);
	Chain* pchain2 = ProteinManager::getInstance()->getOrAddChain(pdb->pdbCode, occupant, chain2);
	map<int, AminoAcid*> aminos = ProteinManager::getInstance()->getAminoAcids(pdb->pdbCode, occupant, chain1);
	vector<Atom*> calphas = ProteinManager::getInstance()->getCAlphas(pdb->pdbCode, occupant, chain1);

	for (unsigned int i = 0; i < calphas.size(); ++i)
	{
		Atom* a = calphas[i];
		AminoAcid* aa = aminos[a->aminoId];
		stringstream ss;
		ss << "Distances for: chain " << chain1 << ":" << a->atomId << ":" << a->aminoId << ":" << aa->aminoCode;
		LogFile::getInstance()->writeMessage(ss.str());
				
		vector<Atom*> atomsb = pchain2->getCAlphas(atomA);
		map<int, AminoAcid*> aminosb = ProteinManager::getInstance()->getAminoAcids(pdb->pdbCode, occupant, chain2);
		for (unsigned int j = 0; j < atomsb.size(); ++j)
		{
			Atom* b = atomsb[j];
			AminoAcid* ab = aminosb[b->aminoId];
			double distance = a->atomicDistance(b,false);
			if (distance < 25) //TODO this should be configurable
			{				
				report << getRow(aa, a, ab, b, distance,true,0,0,atomA + "-" + atomB) << "\n";
			}
		}			
	}
	ofstream outfile(fileName);
	if (outfile.is_open())
	{
		outfile << report.str();
	}
	
}

/*void CAlphaReport::printMultiReport(PDBFile* pdb1, PDBFile* pdb2, string occupant, string fileName, bool shifted)
{//produce data frame report for R reporting

	LogFile::getInstance()->writeMessage("Starting C Aplpha distance map");
	
	stringstream report;
	report << getHeader() << "\n";
	map<string, Chain*> chains1 = ProteinManager::getInstance()->getChains(pdb1->pdbCode, occupant);
	map<string, Chain*> chains2 = ProteinManager::getInstance()->getChains(pdb2->pdbCode, occupant);
	for (map<string, Chain*>::iterator iter = chains1.begin(); iter != chains1.end(); ++iter)
	{
		Chain* chain = iter->second;
		string chainid = iter->first;
		map<int, AminoAcid*> aminos = ProteinManager::getInstance()->getAminoAcids(pdb1->pdbCode, occupant, chainid);
		vector<Atom*> calphas = ProteinManager::getInstance()->getCAlphas(pdb1->pdbCode, occupant, chainid);

		for (unsigned int i = 0; i < calphas.size(); ++i)
		{
			Atom* a = calphas[i];
			AminoAcid* aa = aminos[a->aminoId];
			stringstream ss;
			ss << "Distances for: chain " << chain->chainId << ":" << a->atomId << ":" << a->aminoId << ":" << aa->aminoCode;
			LogFile::getInstance()->writeMessage(ss.str());

			for (map<string, Chain*>::iterator iterb = chains2.begin(); iterb != chains2.end(); ++iterb)
			{
				Chain* chainb = iterb->second;
				vector<Atom*> atomsb = chainb->getCAlphas("CA");
				map<int, AminoAcid*> aminosb = ProteinManager::getInstance()->getAminoAcids(pdb2->pdbCode, occupant, chainb->chainId);
				unsigned int start = 0;								
				for (unsigned int j = start; j < atomsb.size(); ++j)
				{
					Atom* b = atomsb[j];
					AminoAcid* ab = aminosb[b->aminoId];
					double distance = a->atomicDistance(b,shifted);
					if (distance < 25) //TODO this should be configurable					
						report << getRow(aa, a, ab, b, distance,false, lastResiduesA, lastResiduesB) << "\n";
				}
			}
		}
	}
	ofstream outfile(fileName);
	if (outfile.is_open())
	{
		outfile << report.str();
	}
	
}*/

string CAlphaReport::getRow(AminoAcid * aa, Atom* a, AminoAcid* ab, Atom* b, double distance, bool singleChain, int previousResiduesA, int previousResiduesB, string atom_types)
{
	int aid = aa->aminoId + previousResiduesA;
	int bid = ab->aminoId + previousResiduesB;
	if (singleChain)
	{
		aid = aa->aminoId;
		bid = ab->aminoId;
	}
	
	stringstream report;
	//pdb_code
	report << aa->pdbCode << ",";
	//amino_code
	report << aa->aminoCode << ",";	
	//amino_no
	report << aa->aminoId << ",";
	//chain
	report << aa->chainId << ",";	
	//residue_no
	report << aid << ",";
	//atom_no
	report << a->atomId << ",";
	//occupant
	report << "A,";
	//ss_psu
	report << aa->getSS() << ",";
	
	//amino_code_b
	report << ab->aminoCode << ",";
	//amino_no_b
	report << ab->aminoId << ",";
	//chain
	report << ab->chainId << ",";
	//residue_no_b
	report << bid << ",";
	//atom_no_b
	report << b->atomId << ",";
	//occupant_b
	report << "A,";
	//ss_psu_b
	report << ab->getSS() << ",";
	//geo_atoms
	report << atom_types << ",";
	//geo_type
	report << "CONTACT,";
	//geo_value
	report << distance;	
	return report.str();
}

string CAlphaReport::getHeader()
{
	return "pdb_code,amino_code,amino_no,chain,residue_no,atom_no,occupant,ss_psu,amino_code_b,amino_no_b,chain_b,residue_no_b,atom_no_b,occupant_b,ss_psu_b,geo_atoms,geo_type,geo_value";
	//return "Amino1,Id1,Chain1,SS1,Hydro1,Donicity1,Chemical1,Polar1,Amino2,Id2,Chain2,SS2,Hydro2,Donicity2,Chemical2,Polar2,Distance";
}

