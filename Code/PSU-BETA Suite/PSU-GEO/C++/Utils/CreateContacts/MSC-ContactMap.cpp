// MSC-CreatePDBGeometry.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string>
#include <PDBFile.h>
#include <ProteinManager.h>
#include <GeometricalDataReport.h>
#include <CSVFile.h>
#include <LogFile.h>
#include <CAlphaReport.h>

using namespace std;

int main()
{

	// ***********************************************
	// * USER UNPUT ******** 
	vector<string> pdblists;
	

	// EXTRA Set
	pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\extra_yes_annotated0_5.csv");

	//High set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\high3_yes_annotated1_5.csv");	
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\high3_yes_annotated2_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\high3_yes_annotated3_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\high3_yes_annotated4_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\high3_yes_annotated5_5.csv");
	
	//2019 set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2019_yes_annotatedA.csv");	
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2019_yes_annotatedB.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2019_yes_annotatedC.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2019_yes_annotatedD.csv");
	
	//2018 set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated1_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated2_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated3_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated4_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated5_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated6_6.csv");
	
	vector<string> existslists;
	//existslists.push_back("F:\\Code\\BbkDatabase\\tbl2_geo_contact\\DataSets\\Version2\\12Jun20\\");

	string pdbdir = "F:\\Code\\BbkTransfer\\pdbfiles\\pdbdata\\";
	string outputdir = "F:\\Code\\BbkDatabase\\tbl2_geo_contact\\DataSets\\Version2\\16Jun20\\";

	unsigned int start = 1; //default = 1, for memory errors

	vector<string> contactsA;
	vector<string> contactsB;
	
	contactsA.push_back("CA");
	contactsB.push_back("CA");

	contactsA.push_back("CB");
	contactsB.push_back("CB");

	contactsA.push_back("SG");
	contactsB.push_back("SG");

	contactsA.push_back("N");
	contactsB.push_back("O");

	double max_distance = 6.1;




	//***************************************************************************
   // Execution begins

	//string geoOutput = outputdir + "GeoValues\\";
	//string atomOutput = outputdir + "Atoms\\";
	//string calclist = outputdir + "GeoCalc.csv";
	string aadata = "F:\\PSUA\\Code\\PSU-ALPHA\\Config\\data_aminoinfo.csv";

	bool success = LogFile::getInstance()->setLogFile("logger.txt", outputdir);
	LogFile::getInstance()->writeMessage("********** Starting Geometry calculations for PSU-BETA **************");

	ProteinManager::getInstance()->createAminoAcidData(aadata);
	
	for (unsigned int p = 0; p < pdblists.size(); ++p)
	{
		string pdblist = pdblists[p];

		CSVFile pdblistfile(pdblist, ",", true);

		CAlphaReport car;

		for (unsigned int i = start; i < pdblistfile.fileVector.size(); ++i)
		{
			string pdb = pdblistfile.fileVector[i][0];
			//if the pdb has already been calculated then we don;t want to do it again
			

			//if (pdb == "6SUP")
			//if(notExists)
			{
				stringstream ss;
				ss << "-----" << i << " -" << pdb << "--------";
				ss << "----- " << p << " / " << pdblists.size() << " ---- " << i << " / " << pdblistfile.fileVector.size() << " --- " << pdb << "--------";
				LogFile::getInstance()->writeMessage(ss.str());
				
				//string pdb = "3BVX";
				try				
				{	
					PDBFile* pdbf = nullptr;
					for (unsigned int c = 0; c < contactsA.size(); ++c)
					{
						string contactA = contactsA[c];
						string contactB = contactsB[c];

						string fileName = outputdir + pdb + "_" + contactA + "_" + contactB + "_contact.csv";

						bool notExists = true;
						if (existslists.size() > 0)
						{
							for (unsigned int e = 0; e < existslists.size(); ++e)
							{
								string pdbResult = existslists[e] + pdb + "_" + contactA + "_" + contactB + "_contact.csv";
								CSVFile pdblistfile(pdbResult, ",", false);
								if (pdblistfile.exists)
								{
									notExists = false;
									LogFile::getInstance()->writeMessage("....... Exists " + pdb);
								}
							}
						}

						if (notExists)
						{
							if (pdbf == nullptr)
							{
								pdbf = ProteinManager::getInstance()->getOrAddPDBFile(pdb, pdbdir + pdb + ".pdb");
								pdbf->loadData();
								pdbf->loadAtoms();
								pdbf->loadBonds();
							}

							if (pdbf->loadedText)
							{
								LogFile::getInstance()->writeMessage("---------" + contactA + "-" + contactB);
								car.printReport(pdbf, "A", "", "", contactA, contactB, fileName, max_distance);
							}
							else
							{
								LogFile::getInstance()->writeMessage("....No pdb file " + pdb);
							}
						}
					}
					ProteinManager::getInstance()->deletePdbs();//keep memory clear
				}
				catch (...)
				{
					LogFile::getInstance()->writeMessage("!!! There was an error with this file");
				}
			}
		}
	}
	cout << "Finished";
}


