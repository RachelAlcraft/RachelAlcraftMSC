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
	// ***  USER INPUT *********************************************************
	string inputPath = "F:\\PSUA\\Code\\PSU-ALPHA\\MSC-RemoveSimilarity\\";

	string inputname = "rcsb_pdb_ids_2018.txt";
	string outputname = "2018_nonsim.csv";
	string rejectedname = "2018_sim.csv";
	double resolutionlimit = 0; // 0 for no limit

	// *************************************************************************
	DataFrame data_rejected(inputPath + rejectedname);
	data_rejected.headerVector.push_back("PDB");
	data_rejected.headerVector.push_back("RES");
	data_rejected.headerVector.push_back("SIM");
	data_rejected.headerVector.push_back("SIMRES");

	cout << "Load the files\n";
	CSVFile sim100(inputPath + "bc-100.out", " ", true);
	CSVFile sim95(inputPath + "bc-95.out", " ", true);
	CSVFile sim90(inputPath + "bc-90.out", " ", true);
	CSVFile pdblist(inputPath + inputname, ",", true);
	//CSVFile entries(inputPath + "entries.idx","\t");
	CSVFile cmpd_res(inputPath + "cmpd_res.idx", ";", true);

	//Turn the cmpd_res into a dictionary of pdb to resoltion
	std::cout << "Make a dictionary of pdb-res\n";
	map<string, double> pdb_res;
	for (unsigned int i = 4; i < cmpd_res.fileVector.size(); ++i)
	{
		vector <string> entry = cmpd_res.fileVector[i];
		string pdb = entry[0];
		pdb = pdb.replace(pdb.find("\t"), 1, "");
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
	//simFiles.push_back(sim100);
	//simFiles.push_back(sim95);
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

				if (this_pdb == "3O4P") // then I want a break point to investigate
				{
					int i = 0;
					i = i + 1;
				}
			
				if (pdb_res.find(this_pdb) != pdb_res.end())
				{
					double res = pdb_res[this_pdb];
					if (res == 0)
					{
						// then we don't want it, ir probably is not good data
						if (std::find(remove_pdb.begin(), remove_pdb.end(), high_pdb) == remove_pdb.end())
						{
							if (pdblist.in(this_pdb)) //only include those in our candiate list
							{
								vector<string> observation;
								observation.push_back(this_pdb);
								stringstream ss;
								ss << setprecision(4);
								ss << res;
								observation.push_back(ss.str());
								observation.push_back("ZERO");
								observation.push_back("");
								data_rejected.fileVector.push_back(observation);
							}

							remove_pdb.push_back(this_pdb);
						}

					}
					else if (resolutionlimit > 0 && res > resolutionlimit)
					{
						// then we don't want it
						if (std::find(remove_pdb.begin(), remove_pdb.end(), high_pdb) == remove_pdb.end())
						{
							if (pdblist.in(this_pdb)) //only include those in our candiate list
							{
								vector<string> observation;
								observation.push_back(this_pdb);
								stringstream ss;
								ss << setprecision(4);
								ss << res;
								observation.push_back(ss.str());
								observation.push_back("LIMIT");
								observation.push_back("");
								data_rejected.fileVector.push_back(observation);
							}

							remove_pdb.push_back(this_pdb);
						}
					}
					if (res <= high_res) // then we want this not the one currently saved
					{
						if (high_pdb != "" && high_pdb != this_pdb)
						{
							//cout << "excluding " << highpdb << ":" << highres << " in favour of " << pdb << ":" << res << "\n";							
							if (std::find(remove_pdb.begin(), remove_pdb.end(), high_pdb) == remove_pdb.end())
							{
								if (pdblist.in(high_pdb)) //only include those in our candiate list
								{
									vector<string> observation;
									observation.push_back(high_pdb);
									stringstream ss;
									ss << setprecision(4);
									ss << res;
									stringstream ssh;
									ssh << setprecision(4);
									ssh << high_res;
									observation.push_back(ssh.str());
									observation.push_back(this_pdb);
									observation.push_back(ss.str());
									data_rejected.fileVector.push_back(observation);
								}

								remove_pdb.push_back(high_pdb);
							}
						}

						high_res = res;
						high_pdb = this_pdb;

					}
					
					/*else // we want to get rid of this one
					{
						if (high_pdb != this_pdb)
						{
							//cout << "excluding " << pdb << ":" << res << " in favour of " << highpdb << ":" << highres << "\n";
							if (std::find(remove_pdb.begin(), remove_pdb.end(), this_pdb) == remove_pdb.end())
							{
								if (pdblist.in(this_pdb)) //only include those in our candiate list
								{
									vector<string> observation;
									observation.push_back(this_pdb);
									stringstream ss;
									ss << setprecision(2);
									ss << res;									
									observation.push_back(ss.str());
									observation.push_back(high_pdb);
									data_rejected.fileVector.push_back(observation);
								}

								remove_pdb.push_back(this_pdb);
							}
						}
					}*/
				}
				else
				{
					//is it safest to remove this then if there is no resolution? Most likely not x-ray.
					if (std::find(remove_pdb.begin(), remove_pdb.end(), this_pdb) == remove_pdb.end())
					{
						if (pdblist.in(this_pdb)) //only include those in our candiate list
						{
							vector<string> observation;
							observation.push_back(this_pdb);
							observation.push_back("NONE");
							observation.push_back(high_pdb);
							observation.push_back("");
							data_rejected.fileVector.push_back(observation);
						}

						remove_pdb.push_back(this_pdb);
					}
				}
				//}
			}
		}
	}

	//now get a list of all the highest resoltuon structures, but don't use any in the delete list	
	std::cout << "Now get all high res structures list\n";
	DataFrame data_nonsim(inputPath + outputname);
	data_nonsim.headerVector.push_back("PDB");
	data_nonsim.headerVector.push_back("RES");
	int pdbcount = pdb_res.size();
	int count = 0;
	for (map<string, double>::iterator iter = pdb_res.begin(); iter != pdb_res.end(); ++iter)
	{
		++count;
		cout << "  " << count << "/" << pdbcount << "\n";
		string pdb = iter->first;
		double res = iter->second;

		if (pdb == "1PJX") // then I want a break point to investigate
		{
			int i = 0;
			i = i + 1;
		}

		if (resolutionlimit == 0 || (resolutionlimit > 0 && res <= resolutionlimit))
		{
			if (pdblist.in(pdb)) //only include those in our candiate list
			{
				//check if it is in the delete list
				//if (remove_pdb.find(pdb) == remove+pdb.end())
				if (std::find(remove_pdb.begin(), remove_pdb.end(), pdb) == remove_pdb.end())
				{
					//then add it to our list
					vector<string> observation;
					observation.push_back(pdb);
					stringstream ss;
					ss << setprecision(4);
					ss << res;
					observation.push_back(ss.str());
					data_nonsim.fileVector.push_back(observation);

				}
			}
		}
	}

	//finally print the list of pdb files that are high res and not 100% sequence similar
	cout << "Now print\n";
	data_nonsim.print();
	data_rejected.print();



	cout << "Completed High Res file manipulation";

}

