// MSC-HighResList.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

/*
This is an unsatisfactory text parsing of some large fields from the pbd 
I would have preferred to use R but it took too long
This is a terrible piece of code written only because I am too ill to think properly. It will still work.
It is just a 1-off to get a unique list of high res structures from the pdb that are not 
identical to others via the 100% similarity file
That is in chains though so this I'm truncating them to do unique pdb files
Vaguely thining where a chain in a file is 100% similar to a chain in another
we only need 1 of them
The files are taken from: https://www.rcsb.org/pages/general/summaries and https://www.rcsb.org/pages/download/ftp
*/

#include <iostream>
#include <CSVFile.h>
#include <algorithm>
#include <map>
#include <DataFrame.h>
#include <sstream>
#include <iomanip>
//#include <PDBFile.h>

using namespace std;

int main()
{
	const double HIGH_RES = 1.3;
	string inputPath = "F:\\PSUA\\Code\\PSU-ALPHA\\MSC-HighResList\\";

	cout << "Load the files\n";
	CSVFile sim100(inputPath + "bc-100.out"," ",true);
	CSVFile sim95(inputPath + "bc-95.out", " ", true);
	CSVFile sim90(inputPath + "bc-90.out", " ", true);
	//CSVFile entries(inputPath + "entries.idx","\t");
	CSVFile cmpd_res(inputPath + "cmpd_res.idx",";",true);

//Turn the cmpd_res into a dictionary of pdb to resoltion
	std::cout << "Make a dictionary of pdb-res\n";
	map<string, double> pdb_res;
	for (unsigned int i = 4; i < cmpd_res.fileVector.size(); ++i)
	{
		vector <string> entry = cmpd_res.fileVector[i];
		string pdb = entry[0];
		pdb = pdb.replace(pdb.find("\t"),1, "");
		string strres = entry[1];		
		
		double res = atof(strres.c_str());
		if (res < 0.0000001)//arbitrary small number
		{
			std::cout << "Not x-ray " << pdb << "\n";
		}
		else
		{
			if (pdb_res.find(pdb) == pdb_res.end())
			{
				pdb_res.insert(pair<string, double>(pdb, res));
			}
		}		
	}


// turn the similarities desired into into a unique set
	vector<CSVFile> simFiles;
	simFiles.push_back(sim100);
	simFiles.push_back(sim95);
	simFiles.push_back(sim90);	
	vector<string> remove_pdb;
	for (unsigned int s = 0; s < simFiles.size(); ++s)
	{
		CSVFile simi = simFiles[s];
		std::cout << "Sim into a unique set\n";
		for (unsigned int i = 0; i < simi.fileVector.size(); ++i)
		{
			std::cout << "i=" << i << "\n";
			vector<string> unique_in_row;
			string high_pdb = "";
			double high_res = 100;
			string this_pdb;
			vector<string> this_row = simi.fileVector[i];

			for (unsigned int j = 0; j < this_row.size(); ++j)
			{
				string pdb = this_row[j]; // but this is a chain, I want just the pdb
				this_pdb = pdb.substr(0, 4);
				
				//if (std::find(unique_in_row.begin(), unique_in_row.end(), pdb) == unique_in_row.end())
				//{
					//unique_in_row.push_back(pdb);
				//}
				//Now which is the highest resolution of these
				//double highres = 100;
				//string highpdb = "";
				//for (unsigned int r = 0; r < unique_in_row.size(); ++r)
				//{
				//	string pdb = unique_in_row[r];
					if (pdb_res.find(this_pdb) != pdb_res.end())
					{
						double res = pdb_res[this_pdb];
						if (res < high_res) // then we want this not the one currently saved
						{							
							if (high_pdb != "")
							{
								//cout << "excluding " << highpdb << ":" << highres << " in favour of " << pdb << ":" << res << "\n";							
								if (std::find(remove_pdb.begin(), remove_pdb.end(), high_pdb) == remove_pdb.end())
								{
									remove_pdb.push_back(high_pdb);
								}
							}

							high_res = res;
							high_pdb = this_pdb;
							
						}
						else // we want to get rid of this one
						{
							//cout << "excluding " << pdb << ":" << res << " in favour of " << highpdb << ":" << highres << "\n";
							if (std::find(remove_pdb.begin(), remove_pdb.end(), this_pdb) == remove_pdb.end())
							{
								remove_pdb.push_back(this_pdb);
							}
						}
					}
					else
					{
						//is it safest to remove this then if there is no resolution? Most likely not x-ray.
						if (std::find(remove_pdb.begin(), remove_pdb.end(), this_pdb) == remove_pdb.end())
						{
							remove_pdb.push_back(this_pdb);
						}
					}
				//}
			}
		}
	}

	//now get a list of all the highest resoltuon structures, but don't use any in the delete list	
	std::cout << "Now get all high res structures list\n";
	DataFrame data_highres(inputPath + "highres_and_unique.txt");
	data_highres.headerVector.push_back("PDB");
	data_highres.headerVector.push_back("RES");
	int pdbcount = pdb_res.size();
	int count = 0;
	for (map<string, double>::iterator iter = pdb_res.begin(); iter != pdb_res.end(); ++iter)
	{
		++count;
		cout << "  " << count << "/" << pdbcount << "\n";
		string pdb = iter->first;
		double res = iter->second;

		if (res <= HIGH_RES)
		{
			//check if it is in the delete list
			if (std::find(remove_pdb.begin(), remove_pdb.end(), pdb) == remove_pdb.end())
			{
				//then add it to our list
				vector<string> observation;
				observation.push_back(pdb);
				stringstream ss;
				ss << setprecision(2);
				ss << res;
				observation.push_back(ss.str());
				data_highres.fileVector.push_back(observation);
				
			}
		}
	}

//finally print the list of pdb files that are high res and not 100% sequence similar
	cout << "Now print\n";
	data_highres.print();



	cout << "Completed High Res file manipulation";
    
}

