// MSC-CreatePDBGeometry.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string>
#include <filesystem>
#include <PDBFile.h>
#include <ProteinManager.h>
#include <GeometricalDataReport.h>
#include <CSVFile.h>
#include <LogFile.h>

using namespace std;

int main()
{

	// ***********************************************
	// * USER UNPUT ******** 
	vector<string> pdblists;		
	
	// EXTRA Set
	pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\extra_yes_annotated0_0.csv");	
	
	// HIGH Set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\high3_yes_annotated1_5.csv");	
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\high3_yes_annotated2_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\high3_yes_annotated3_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\high3_yes_annotated4_5.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\IN\\high3_yes_annotated5_5.csv");

	// 2019 Set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated1_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated2_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated3_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated4_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated5_6.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotated6_6.csv");

	// 2018 Set
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotatedA.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotatedB.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotatedC.csv");
	//pdblists.push_back("F:\\Code\\BbkProject\\Thesis\\Method\\02_DataSets\\2018_yes_annotatedD.csv");
	
	vector<string> existslists;
	//existslists.push_back("F:\\Code\\BbkDatabase_notsynched\\tbl2_geo_measure_and_atom\\DataSets\\Version5\\12Jun20\\");
	//existslists.push_back("F:\\Code\\BbkDatabase\\tbl2_geo_measure_and_atom\\DataSets\\Version5\\29Jun20\\");
	
	string pdbdir = "F:\\Code\\BbkTransfer\\pdbfiles\\pdbdata\\";			
	string outputdir = "F:\\Code\\BbkDatabase\\tbl2_geo_measure_and_atom\\DataSets\\Version5\\29Jun20\\";

	bool runCore = true;
	bool runExtra = false;
	bool runAtoms = true;

	
	

	 //***************************************************************************
	// Execution begins

	//string geoOutput = outputdir + "GeoValues\\";
	//string atomOutput = outputdir + "Atoms\\";
	string calclist = outputdir + "GeoCalc.csv";		
	string aadata = "F:\\PSUA\\Code\\PSU-ALPHA\\Config\\data_aminoinfo.csv";
	
	bool success = LogFile::getInstance()->setLogFile("logger.txt", outputdir);
	LogFile::getInstance()->writeMessage("********** Starting Geometry calculations for PSU-BETA **************");
	
	ProteinManager::getInstance()->createAminoAcidData(aadata);
	
	CSVFile geoFileCore(calclist, ",", true);
	
	for (unsigned int p = 0; p < pdblists.size(); ++p)
	{
		string pdblist = pdblists[p];
		CSVFile pdblistfile(pdblist, ",", true);


		GeometricalDataReport gdr(geoFileCore.fileVector);
		

		for (unsigned int i = 1; i < pdblistfile.fileVector.size(); ++i)
		{
			string pdb = pdblistfile.fileVector[i][0];

			stringstream ss;
			ss << "----- " << p << " / " << pdblists.size() << " ---- " << i << " / " << pdblistfile.fileVector.size() << " --- " << pdb << "--------";
			LogFile::getInstance()->writeMessage(ss.str());

			//if the pdb has already been calculated then we don;t want to do it again
			bool notExists = true;
			if (existslists.size() > 0)
			{
				for (unsigned int e = 0; e < existslists.size(); ++e)
				{
					string pdbResult = existslists[e] + "core\\" + pdb + "_A_cgeo.txt";
					CSVFile pdblistfile(pdbResult, ",", false);
					if (pdblistfile.exists)
					{
						notExists = false;
						LogFile::getInstance()->writeMessage("....... Exists " + pdb);
					}
				}
			}
			
			//if(pdb == "1DG6")
			//if(i > 1459)
			if (notExists)
			{				
				//string pdb = "3BVX";
				CSVFile pdbfile(pdbdir + pdb + ".pdb", ",", false);
				if (pdbfile.exists)
				{
					PDBFile* pdbf = ProteinManager::getInstance()->getOrAddPDBFile(pdb, pdbdir + pdb + ".pdb");
					pdbf->loadData();
					pdbf->loadAtoms();
					pdbf->loadBonds();
					gdr.printReport(pdbf, outputdir, runCore, runExtra, runAtoms);
					ProteinManager::getInstance()->deletePdbs();//keep memory clear		
				}
				else
				{
					LogFile::getInstance()->writeMessage("....No pdb file " + pdb);
				}
			}
		}
	}
	LogFile::getInstance()->writeMessage("Completed");
	cout << "Finished";    
}


