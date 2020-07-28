#include "GeometricalAggregationReport.h"
#include <string>
#include <iostream>
#include <vector>
#include <Windows.h> // TODO this is windows only which is not what I want ultimately, have not succedded in using boost yet.

#include <LogFile.h>
#include <CSVFile.h>
#include <map>
#include <FoldersFiles.h>
#include <GeometryObservation.h>

using namespace std;

void GeometricalAggregationReport::printReport(string datadir)
{
	LogFile::getInstance()->writeMessage("Starting Aggregation report for " + datadir);
	vector<string> files = FoldersFiles::getFilesWithinFolder(datadir);
	for (unsigned int i = 0; i < files.size(); ++i)
	{
		files[i] = datadir + files[i];
	}
	vector<string> aminos;
	aminos.push_back("");
	aminos.push_back("ALA");
	aminos.push_back("CYS");
	aminos.push_back("ASP");
	aminos.push_back("GLU");
	aminos.push_back("PHE");
	aminos.push_back("GLY");
	aminos.push_back("HIS");
	aminos.push_back("ILE");
	aminos.push_back("LYS");
	aminos.push_back("LEU");
	aminos.push_back("MET");
	aminos.push_back("ASN");
	aminos.push_back("PRO");
	aminos.push_back("GLN");
	aminos.push_back("ARG");
	aminos.push_back("SER");
	aminos.push_back("THR");
	aminos.push_back("VAL");
	aminos.push_back("TRP");
	aminos.push_back("TYR");
	for (unsigned int a = 0; a < aminos.size(); ++a)		
		printReport(files,datadir,aminos[a]);
}

void GeometricalAggregationReport::printReport(vector<string> files, string outdir, string aa)
{
	LogFile::getInstance()->writeMessage("Starting Aggregation report for given files");	
	//map<string,map<string, vector<double>>> probabilities;
	//map<string, vector<GeometryObservation>> probabilities;
	vector<GeometryObservation> probabilities;
	for (unsigned int i = 0; i < files.size(); ++i)
	{
		stringstream status;
		status << i << " out of " << files.size() << " ";
		string file = files[i];
		LogFile::getInstance()->writeMessage(status.str() + files[i]);
		try
		{					
			CSVFile csv(file,",",true);
			for (unsigned int i = 1; i < csv.fileVector.size(); ++i) // TODO a bit hard coded, skipping the header and we know we want 1,3,4,5,6 then 7 is the value
			{
				//Headers of the geofile				
				//PdbCode, Chain, AminoAcid, AminoNo, PdbAtoms, SecStruct, GeoType, ExperimentalMethod, GeoAtoms, AminoCodes, Value
				if (csv.fileVector[i].size() > 7)
				{
					GeometryObservation geo;					
					geo.pdbCode = csv.fileVector[i][0]; //eg 4REK
					//no chain
					geo.aminoCode = csv.fileVector[i][2]; //eg ALA
					geo.aminoNo = csv.fileVector[i][3]; //eg 4					
					geo.pdbAtoms = csv.fileVector[i][4]; // 1-2-4
					geo.secStruc = csv.fileVector[i][5]; //eg A = alpha helix this is dummy code for now
					geo.geoType = csv.fileVector[i][6]; //eg ANGLE															
					//no exp method
					geo.geoAtoms = csv.fileVector[i][8]; // eg N-Ca
					geo.allAAs = csv.fileVector[i][9]; // eg N-Ca

					if (geo.aminoCode == aa)
					{
						geo.value = atof((csv.fileVector[i][10]).c_str());					
						probabilities.push_back(geo);
					}
				}
				else
				{
					LogFile::getInstance()->writeMessage("Invalid data for creating geometric aggregation");
				}
			}
		}
		catch (...)
		{
			LogFile::getInstance()->writeMessage("!!!Error");
		}
	}

	//now print out the probability distribution file per amino acid so it is easy to look at
	
	
	//for (map<string, vector<GeometryObservation>>::iterator iter = probabilities.begin(); iter != probabilities.end(); ++iter)
	{
		try
		{
			//TODO better to make it a dataframe by having
			// AA,Exmp_meth,geo type, SS,atoms,values as a : delim list
			// Then the prob dist can be got at whatever preferre granularity
			stringstream report;
			//report << "PdbCode,AminoAcid,GeoType,GeoAtoms,PdbAtoms,Value\n";
			report << "PdbCode,AminoAcid,AminoNo,AtomNos,SecStruct,GeoType,GeoAtoms,AminoCodes,Value\n";					
			for (unsigned int i = 0; i < probabilities.size(); ++i)
			{
				GeometryObservation geo = probabilities[i];
				report << geo.pdbCode << ",";
				report << geo.aminoCode << ",";				
				report << geo.aminoNo << ",";				
				report << geo.pdbAtoms << ",";
				report << geo.secStruc << ",";
				report << geo.geoType << ",";
				report << geo.geoAtoms << ",";				
				report << geo.allAAs << ",";
				report << geo.value;				
				report << "\n";
			}

			string filename = outdir + aa + "_geoprobdist.csv";
			ofstream outfile(filename);
			if (outfile.is_open())
			{
				LogFile::getInstance()->writeMessage("Printing " + filename);
				outfile << report.str();
			}
		}
		catch (...)
		{
			LogFile::getInstance()->writeMessage("!!! Error printing aggregation");
		}
	}

	

}

/*vector<string> GeometricalAggregationReport::getFilesWithinFolder(string folder)
{//https://stackoverflow.com/questions/612097/how-can-i-get-the-list-of-files-in-a-directory-using-c-or-c
	vector<string> names;
	string search_path = folder + "*.*";
	wstring wrpath = StringManip::utf8ToUtf16(search_path);
	LPCWSTR lpr = wrpath.c_str();
	WIN32_FIND_DATA fd;
	HANDLE hFind = ::FindFirstFile(lpr, &fd);
	if (hFind != INVALID_HANDLE_VALUE) 
	{
		do {
			// read all (real) files in current folder
			// , delete '!' read other 2 default folder . and ..
			if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) 
			{
				wstring fs = fd.cFileName;				
				string s = StringManip::ws2s(fs);
				names.push_back(s);
			}
		} while (::FindNextFile(hFind, &fd));
		::FindClose(hFind);
	}
	return names;
}*/


