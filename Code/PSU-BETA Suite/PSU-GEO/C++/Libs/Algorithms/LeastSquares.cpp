#include "LeastSquares.h"
#include <ProteinManager.h>
#include <LogFile.h>

#include "btl_least_squares.h"
#include "btl_matrix.h"
#include "btl_numeric_vector.h"
#include "btl_matrix_algorithms.h"
#include <btl_sequence_algorithms.h>

using namespace btl;

LeastSquares::LeastSquares(PDBFile* pdb1, PDBFile* pdb2, bool align)
{
	PDB1 = pdb1;
	PDB2 = pdb2;	
	Alignment = align;
	setupAtomPairs();
}

void LeastSquares::setupAtomPairs()
{//For a very first implementation this will just be the best matching cAlphas
	vector<Atom*> calphas1 = ProteinManager::getInstance()->getCAlphas(PDB1->pdbCode,"A","CA");
	vector<Atom*> calphas2 = ProteinManager::getInstance()->getCAlphas(PDB2->pdbCode,"A","CA");

	
	if (!Alignment)
	{
		int maxposs_calphas = min(calphas1.size(), calphas2.size());
		for (int i = 0; i < maxposs_calphas; ++i)
		{
			_atomPairsAlignment.push_back(AtomPair(calphas1[i], calphas2[i]));
			reportStream << "RMSD Match: " + calphas1[i]->getDescription() + " " + calphas2[i]->getDescription() << "\n";
			//LogFile::getInstance()->writeMessage("RMSD Match: " + calphas1[i]->getDescription() + " " + calphas2[i]->getDescription());
		}
	}
	else
	{//use alignment file to match off
		string seq1 = PDB1->getStructureVersion("A")->getSequence();
		string seq2 = PDB2->getStructureVersion("A")->getSequence();
		/*FOR TESTING*/
		//seq1 = "AADDE";
		//seq2 = "AADE";
		//seq2 = "CTNETTL";
		//seq1 = "KLP";
		unsigned int safeSize = max(seq1.size(), seq2.size())*3;		
		string output = "";
		output.resize(safeSize);				
		float score = 0.0;
		
		//From BTL
		score = needleman_wunsch_similarity(seq1.begin(), seq1.end(), seq2.begin(), seq2.end(), 1, 0, 0, 0, score);		
		needleman_wunsch_alignment(seq1.begin(), seq1.end(), seq2.begin(), seq2.end(), 1, 0, 0, 0, output.begin());		

		reportStream << "NW Alignment score = " << score << "\n";
		
		
		//Now create CAlphas based on the alignment
		vector<AminoAcid*> aminos1;
		vector<AminoAcid*> aminos2;
		map<string, Chain*> chains1 = PDB1->getStructureVersion("A")->getChains();
		map<string, Chain*> chains2 = PDB2->getStructureVersion("A")->getChains();
		for (map<string, Chain*>::iterator iter = chains1.begin(); iter != chains1.end(); ++iter)
		{
			map<int, AminoAcid*> aminos = iter->second->getAminoAcids();
			for (map<int, AminoAcid*>::iterator aiter = aminos.begin(); aiter != aminos.end(); ++aiter)			
				aminos1.push_back(aiter->second);
		}
		for (map<string, Chain*>::iterator iter = chains2.begin(); iter != chains2.end(); ++iter)
		{
			map<int, AminoAcid*> aminos = iter->second->getAminoAcids();
			for (map<int, AminoAcid*>::iterator aiter = aminos.begin(); aiter != aminos.end(); ++aiter)
				aminos2.push_back(aiter->second);
		}

		
		stringstream al1, al2;
		unsigned int i = 0;
		while (i < output.size() - 1)
		{
			al1 << output[i];
			al2 << output[i+1];
			i += 2;
		}		
		reportStream << al1.str() << "\n";
		reportStream << al2.str() << "\n";
		string str1 = al1.str();
		string str2 = al2.str();
		
		unsigned int a = 0;
		unsigned int b = 0;
		
		//al1 and al2 must be the same size
		if (str1.size() == str2.size())
		{
			for (unsigned int i = 0; i < str1.size(); ++i)
			{
				char seq1char = str1[i];
				char seq2char = str2[i];
				if (!(seq1char == '\0' || seq2char == '\0'))
				{
					al1 << seq1char;
					al2 << seq2char;
					bool gaps = false;
					if (seq1char == ' ')
						gaps = true;
					if (seq2char == ' ')
						gaps = true;
					if (!gaps && a < aminos1.size() && b < aminos2.size())
					{
						Atom* a1 = aminos1[a]->getCAlpha("CA");
						Atom* a2 = aminos2[b]->getCAlpha("CA");
						_atomPairsAlignment.push_back(AtomPair(a1, a2));
						LogFile::getInstance()->writeMessage("RMSD Match: " + a1->getDescription() + " " + a2->getDescription());
						reportStream << "RMSD Match: " + a1->getDescription() + " " + a2->getDescription() << "\n";
					}
					if (seq1char != ' ')
						++a;
					if (seq2char != ' ')
						++b;
				}
			}
		}
		else
		{
			LogFile::getInstance()->writeMessage("Error in sequence alignment, they don't match");
		}
		
		

	}
}

double LeastSquares::calculateRMSDLeastSquares()
{
	//Create vectors for the btl algorithm
	vector<double> vA;
	vector<double> vB;
	for (unsigned int i = 0; i < _atomPairsAlignment.size(); ++i)
	{
		GeoCoords a = _atomPairsAlignment[i].a1->coords;
		GeoCoords b = _atomPairsAlignment[i].a2->coords;
		vA.push_back(a.x);
		vA.push_back(a.y);
		vA.push_back(a.z);
		vB.push_back(b.x);
		vB.push_back(b.y);
		vB.push_back(b.z);
	}

	double rmsd = 0.0;
	rmsd = lsqfit(vA.begin(), vA.end(), vB.begin(), vB.end(), rmsd);
	return rmsd;
}

void LeastSquares::applyRMSDLeastSquares()
{
	//Create vectors for the btl algorithm, but this time we need to apply the matrices to all the atoms in our structure
	vector<double> vAForAlignment;
	vector<double> vBForAlignment;
	for (unsigned int i = 0; i < _atomPairsAlignment.size(); ++i)
	{
		GeoCoords a = _atomPairsAlignment[i].a1->coords;
		GeoCoords b = _atomPairsAlignment[i].a2->coords;
		vAForAlignment.push_back(a.x);
		vAForAlignment.push_back(a.y);
		vAForAlignment.push_back(a.z);
		vBForAlignment.push_back(b.x);
		vBForAlignment.push_back(b.y);
		vBForAlignment.push_back(b.z);
	}

	//Build vectors of all atoms
	vector<double> vAForAll;	
	vector<Atom*> atoms = ProteinManager::getInstance()->getAtoms(PDB1->pdbCode,"A");
	for (unsigned int i = 0; i < atoms.size(); ++i)
	{
		Atom* atm = atoms[i];
		vAForAll.push_back(atm->coords.x);
		vAForAll.push_back(atm->coords.y);
		vAForAll.push_back(atm->coords.z);
	}
	

	//Code copied from BTL to access the matrices for transfromation to entire structure
	{
		// Do the superposition the long way in order to demonstrate the vector and matrix algorithms 
		// The geometric centre of each structure is declared as a BTL numeric_vector with 3 elements of
		// BTL_REAL(0.0) (the default). The coordinates of the centres are calculated using the generic 
		// BTL centroid algorithm is in this case operating on both STL and BTL vectors.
		numeric_vector<> centreA, centreB;
		centroid(vAForAlignment.begin(), vAForAlignment.end(), centreA.begin());
		centroid(vBForAlignment.begin(), vBForAlignment.end(), centreB.begin());

		// Move protein A such that the protein centres are superimposed using the generic BTL algorithm `translate'
		numeric_vector<> translation = centreB - centreA;
		translate(vAForAlignment.begin(), vAForAlignment.end(), translation.begin());
		// ALSO TRANSLATE ALL #############################################################################
		translate(vAForAll.begin(), vAForAll.end(), translation.begin());

		// Determine and perform the rotation necessary to superimpose structures
		// First calculate the Kearsley matrix and determine its eigenvalues and eigenvectors
		matrix<> matfit(4, 4), evector(4, 4); numeric_vector<> evalue(4);
		_kearsley_matrix(vAForAlignment.begin(), vAForAlignment.end(), vBForAlignment.begin(), vBForAlignment.end(), matfit.begin());

		eigen_solution(matfit.begin(), matfit.end(), 4, evector.begin(), evalue.begin());
		transpose(evector.begin(), evector.end(), 4, evector.begin());
	
		// Then rotate A about its centre in order to effect the superposition
		matrix<> rotation(3, 3);
		rotation_from_fit(evector.begin(), rotation.begin());
		rotate(vAForAlignment.begin(), vAForAlignment.end(), rotation.begin(), centreB.begin());
		// ALSO ROTATE ALL #############################################################################
		rotate(vAForAll.begin(), vAForAll.end(), rotation.begin(), centreB.begin());		

		//Now put the coordinates back over the pdb
		unsigned int j = 0;
		for (unsigned int i = 0; i < atoms.size(); ++i)
		{
			if (j < vAForAll.size()-2)
			{
				Atom* atm = atoms[i];
				atm->shifted_coords.x = vAForAll[j];
				atm->shifted_coords.y = vAForAll[j + 1];
				atm->shifted_coords.z = vAForAll[j + 2];
				j += 3;
			}
			else
			{
				LogFile::getInstance()->writeMessage("error in size of shifted vector for RMSD");
			}
		}
		
	}
}