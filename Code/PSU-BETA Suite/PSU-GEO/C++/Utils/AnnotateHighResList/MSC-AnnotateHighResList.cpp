// MSC-AnnotateHighResList.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <CSVFile.h>
#include <DataFrame.h>
#include <StringManip.h>
#include <sstream>
#include <PDBFile.h>
//#include <LogFile.h>
#include <ProteinManager.h>
#include <LogFile.h>
using namespace std;

/*
This annotates the list of pdbs that are unique and high res with info from their downloaded PDB files
From Mark: their resolution, R and Rfree values and whether or not they have experimental data =structure factors
Also: How many chains, whether there are small molecules
*/

int main()
{
	/*
	This runs in 2 sections because of memory problems which I will fix another time!
	*/

	//string set5label = "HIGHRES";
	int runID = 7;
	int runOf = 7;
	stringstream ss;
	ss << runID << "_" << runOf;
	string runIDx = ss.str();

	//string filePath = "F:\\PSUA\\Code\\PSU-ALPHA\\MSC-RemoveSimilarity\\";
	
	// USER INPUT FILE PATHS AND NAMES	
	string inputname = "F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\nonsim_lists\\2019_nonsim.csv";
	string outputnameYes = "F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\2019_yes_annotated";
	string outputnameNo = "F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\OUT\\2019_no_annotated_mutations";

	bool outputIN = false;
	bool outputOUT = true;
		
	string pdbdir = "F:\\Code\\BbkTransfer\\pdbfiles\\pdbdata\\";

	string aadata = "F:\\PSUA\\Code\\PSU-ALPHA\\Config\\data_aminoinfo.csv";

	// CODE BEGINS
	
	string annPDBFileYes = outputnameYes + runIDx + ".csv";
	string annPDBFileNo = outputnameNo + runIDx + ".csv";

	CSVFile inPDBs(inputname, ",", true);
	DataFrame annPDBsYes(annPDBFileYes);
	DataFrame annPDBsNo(annPDBFileNo);
	
	bool success = LogFile::getInstance()->setLogFile("logger.txt", "F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\");
	
	ProteinManager::getInstance()->createAminoAcidData(aadata);
	
	vector<string> headerVector;

	headerVector.push_back("PDB"); //pdb code
	headerVector.push_back("RES"); //the resolution
	headerVector.push_back("CLASS"); //header class
	headerVector.push_back("COMPLEX"); //is the structure a complex?
	headerVector.push_back("RVALUE"); // the r value
	headerVector.push_back("RFREE");  // the r free value
	headerVector.push_back("OCCUPANCY"); //any atoms with occupancy less than 1?
	headerVector.push_back("BFACTOR"); //is there ever a b factor > 30? Y or N
	headerVector.push_back("HYDROGENS"); //level of detail of resolution such that hydrogen atoms are in the pdb structure
	headerVector.push_back("STRUCFAC"); //are there structure factors in the pdb
	headerVector.push_back("CHAINS"); //How many chains
	headerVector.push_back("RESIDUES"); //how many residies
	headerVector.push_back("NUCLEOTIDES"); //how many nucleotides
	headerVector.push_back("DATE"); //what date was it deposited
	headerVector.push_back("INSTITUTION"); //who deposited it
	headerVector.push_back("SOFTWARE"); //how was it refined?
	headerVector.push_back("SEQUENCE"); //how was it refined?
	headerVector.push_back("EXPMETHOD"); //always xray
	headerVector.push_back("NEGATIVE"); //are there any negatiove amino acid numbers
	headerVector.push_back("BREAKS"); //are there any breaks in the amino numbering
	headerVector.push_back("INSERTIONS"); //are there any insertions due to mutations, eg 3hgp at residue 36
	headerVector.push_back("NCS"); // does it have the NCS model setting
	headerVector.push_back("IDENTICALS"); // are the chains all identical

	//annPDBs.headerVector.push_back("STATUS"); //NA here comments can be annoted later

	if (outputIN)
	{
		annPDBsYes.print(); // this clears it
		annPDBsYes.headerVector = headerVector;
	}
	if (outputOUT)
	{
		annPDBsNo.print(); // this clears it
		annPDBsNo.headerVector = headerVector;
	}

	unsigned int start = 0;
	unsigned int end = inPDBs.fileVector.size();

	if (runID > 0)
	{
		int bit = int(end / runOf);
		start = (runID - 1) * bit;
		end = bit * runID;
		if (runID == runOf)
			end = inPDBs.fileVector.size();
	}
	
	for (unsigned int i = start; i < end; ++i)
	{
		vector<string> observation;
		string pdb = inPDBs.fileVector[i][0];

		//if (pdb == "6J6V")
		{

			
			//string res = inPDBs.fileVector[i][1];
			// header problems mneans I cannot actually use my pdb class or the whole project stops building, needs fixing TODO
			CSVFile pdbfile(pdbdir + pdb + ".pdb", "@", true); //dummy seperator as I want the whole line
			CSVFile structurefile(pdbdir + pdb + "-sf.cif", "@", false); //dummy seperator only checking file exists
			string sf = structurefile.exists ? "Y" : "N";

			string res = "NA";
			string rval = "NA";
			string rfree = "NA";
			string occ = "NA";
			string bfactor = "NA";
			string hyd = "NA";
			string chains = "NA";
			string name = "NA";
			string complex = "NA";
			string residues = "NA";
			string nucleotides = "NA";
			string date = "NA";
			string institution = "NA";
			string software = "NA";
			string sequence = "NA";
			string negative = "NA";
			string breaks = "NA";
			string insertions = "NA";
			string ncs = "NA";
			string identicals = "NA";
			unsigned int iresidues = 0;
			int inucleotides = 0;

			/*
			HEADER    OXIDOREDUCTASE                          17-SEP-98   1BVR
			COMPND   3 CHAIN: A, B, C, D, E, F;
			REMARK   3   R VALUE            (WORKING SET) : 0.161
			REMARK   3   FREE R VALUE                     : 0.178
			*/
			stringstream ss;
			ss << "Annotating " << pdb << " " << i << "/" << end;
			LogFile::getInstance()->writeMessage(ss.str());
			//if (true)
			//{			


			//}
			if (pdbfile.exists)
			{
				//slowly put the functionality into the pdbfile class
				PDBFile* pdbf = ProteinManager::getInstance()->getOrAddPDBFile(pdb, pdbdir + pdb + ".pdb");
				pdbf->loadData();
				pdbf->loadAtoms();
			

				inucleotides = pdbf->nucleotides;
				stringstream ssnuc;
				ssnuc << inucleotides;
				nucleotides = ssnuc.str();


				//occupancy
				bool occupancy = ProteinManager::getInstance()->hasOccupancy(pdb, "A");
				occupancy ? occ = "Y" : occ = "N";

				//BFactor
				double bf = ProteinManager::getInstance()->maxBFactor(pdb, "A");
				stringstream ssbf;
				ssbf.precision(5);
				ssbf << bf;
				bfactor = ssbf.str();

				//hydrogens - level of detail of resolution such that hydrogen atoms are in the pdb structure
				bool hydrogens = ProteinManager::getInstance()->hasHydrogens(pdb, "A");
				hydrogens ? hyd = "Y" : hyd = "N";

				institution = pdbf->institution;
				software = pdbf->software;

				bool nullmodel = pdbf->nullModel;
										
				vector<string> seqs = pdbf->getSequence();
				sequence = "";
				bool differ = false;					
				for (unsigned int r = 0; r < seqs.size(); ++r)
				{
					if (seqs[r].length() > iresidues)
						iresidues = seqs[r].length();
					sequence += seqs[r];
				}
					
				identicals = pdbf->identicalChains() ? "Y" : "N";
				breaks = pdbf->hasBreaks() ? "Y" : "N";
				insertions = pdbf->hasInsertions() ? "Y" : "N";
				negative = pdbf->hasNegativeAminos() ? "Y" : "N";										
				ncs = pdbf->hasNCS() ? "Y" : "N";
					
				stringstream ssres;
				ssres << iresidues; // this is the max chain not the total residues
				residues = ssres.str();

 				rval = pdbf->rvalue;
				rfree = pdbf->rfree;
				res = pdbf->resolution;
				chains = pdbf->maxChain();
				name = pdbf->proteinclass;
				complex = pdbf->inComplex;
				date = pdbf->date;
			}

			observation.push_back(pdb);
			observation.push_back(res);
			observation.push_back(name);
			observation.push_back(complex);
			observation.push_back(rval);
			observation.push_back(rfree);
			observation.push_back(occ);
			observation.push_back(bfactor);
			observation.push_back(hyd);
			observation.push_back(sf);
			observation.push_back(chains);
			observation.push_back(residues);
			observation.push_back(nucleotides);
			observation.push_back(date);
			observation.push_back(institution);
			observation.push_back(software);
			observation.push_back(sequence);
			observation.push_back("XR");
			observation.push_back(negative);
			observation.push_back(breaks);
			observation.push_back(insertions);
			observation.push_back(ncs);
			observation.push_back(identicals);
			//observation.push_back(set_label);
			//choose if in or out
			bool bIn = true;
			if (iresidues <= 30)
				bIn = false;
			if (inucleotides > 0)
				bIn = false;
			//if (breaks == "Y")
			//	bIn = false;
			//if (negative == "Y")
			//	bIn = false;
			//if (identicals == "Y" && ncs == "N")
			//	bIn = false;

			if (bIn) // just trying to remove acccidentally included mutations DELETE			
			{
				if (insertions == "Y" && res != "NA")
					bIn = false;

			}
			else
			{
				bIn = true; // it is not, but we already know that
			}
				

			
			if (bIn)
			{
				if (outputIN)
					annPDBsYes.fileVector.push_back(observation);
			}
			else
			{
				if (outputOUT)
					annPDBsNo.fileVector.push_back(observation);
			}

			ProteinManager::getInstance()->deletePdbs();//keep memory clear

			//Every so often print out to file otherwise it gets too big
			if (i % 100 == 0)
			{
				if (outputIN)
					annPDBsYes.flush();
				if (outputOUT)
					annPDBsNo.flush();
			}						
		}
	}
	LogFile::getInstance()->writeMessage("Success, now printing");
	if (outputIN)
	{
		bool ok = annPDBsYes.flush();
		cout << "Printed YES - " << (ok ? "OK" : "FAILED") << '/n';
	}
	if (outputOUT)
	{
		bool ok = annPDBsNo.flush();
		cout << "Printed NO - " << (ok ? "OK" : "FAILED") << '/n';
	}
}


