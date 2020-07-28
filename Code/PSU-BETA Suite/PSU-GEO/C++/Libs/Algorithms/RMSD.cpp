#include "RMSD.h"
#include <LogFile.h>
#include <ProteinManager.h>
#include <algorithm>
#include <GeoShape.h>



RMSD::RMSD()
{
	PDB1 = nullptr;
	PDB2 = nullptr;
	Fasta = nullptr;
	Optimise = false;
	Alignment = false;
}
RMSD::RMSD(PDBFile* pdb1, PDBFile* pdb2, FastaFile* fasta, bool alignment, bool optimise)
{
	PDB1 = pdb1;
	PDB2 = pdb2;
	Fasta = fasta;
	Alignment = alignment;
	Optimise = optimise;
	SetupCAlphaPairs();
}

void RMSD::SetupCAlphaPairs()
{//For a very first implementation this will just be the best matching cAlphas
	vector<Atom*> calphas1 = ProteinManager::getInstance()->getCAlphas(PDB1->pdbCode,"A","CA");
	vector<Atom*> calphas2 = ProteinManager::getInstance()->getCAlphas(PDB2->pdbCode,"A","CA");
	
	int maxposs_calphas = min(calphas1.size(), calphas2.size());

	if (!Alignment)
	{
		for (int i = 0; i < maxposs_calphas; ++i)
		{			
			_calphaPairs.push_back(CAlphaPair(calphas1[i],calphas2[i]));
			_geo1.addCoords(calphas1[i]->shifted_coords);
			_geo2.addCoords(calphas2[i]->shifted_coords);
			LogFile::getInstance()->writeMessage("RMSD Match: " + calphas1[i]->getDescription() + " " + calphas2[i]->getDescription());
		}
	}
	else
	{//use alignment file to match off

	}
	//Having set up CAlpha pairs we can now calculate the internal distances of each GeoCloud
	_geo1.createDistances();
	_geo2.createDistances();
}



string RMSD::calculateRMSD() 
{
	stringstream ss;
	if (Optimise)
	{
		ss << "Optimised report\n";
		ss << "Initial Value=" << calculateOneRMSD() << "\n";				
		LogFile::getInstance()->writeMessage(ss.str());
		//Dummy attempt at optimisation TODO ALSO TODO if any ever come back as 0 we can stop!
		double best = 0;
		unsigned int hval = 0;
		unsigned int ival = 0;
		unsigned int jval = 0;
		unsigned int kval = 0;		
		unsigned int MAXITER1 = 501;//should be config TODO
		unsigned int MAXITER2 = 3;//should be config TODO
		unsigned int count = 0;
		double total = pow(MAXITER1-1, 2) * pow(MAXITER2-1, 2);
		for (unsigned int h = 1; h < MAXITER1; ++h)
		{
			for (unsigned int i = 1; i < MAXITER2; ++i)
			{
				for (unsigned int j = 1; j < MAXITER1; ++j)
				{
					for (unsigned int k = 1; k < MAXITER2; ++k)
					{
						++count;
						if (count % 1000 == 0)
						{
							stringstream ss;
							ss << "RMSD Opt " << count << "/" << total;
							LogFile::getInstance()->writeMessage(ss.str());
						}
						string report;
						double rmsd = calculateOptimalRMSD(h, i, j, k,report); // -1 is an invalid return value
						if (rmsd >= 0)
						{
							ss << report << "\n\n";
							if (ival == 0 || rmsd < best)
							{
								hval = h;
								ival = i;
								jval = j;
								kval = k;
								//orientation = orient;
								best = rmsd;
							}
						}
						else
						{
							ss << "Invalid at " << h <<","<< i<<"," << j<<"," << k  << "\n\n";
						}
					}
				}
			}
		}
		
		//So we have done a minimum optimisation and we will take the best, calculating it again TODO because I haven't saved it
		string report;
		ss << "Best RMSD Chosen as :\n";
		double rmsd = calculateOptimalRMSD(hval,ival, jval,kval,report);		
		ss << report << "\n";
		ss << "Optimised report: RMSD Value=" << rmsd << "\n";
	}
	else
	{
		ss << "Non optimised report: RMSD Value=" << calculateOneRMSD();
	}
	return ss.str();	
}
double RMSD::calculateOptimalRMSD(int h,int i, int j, int k, string& report/*, int orientation*/)
{
	stringstream ss;
	ss << "Optimising for " << h << ":" << i << ":" << j << ":" << k << "\n";
	GeoTripod tri1, tri2;
	_geo1.makeTripod(tri1,h, i);
	_geo2.makeTripod(tri2,j, k);
	if (tri1.Init && tri2.Init)
	{
		ss << "Tripod 1=" << tri1.info() << "\n";
		ss << "Tripod 2=" << tri2.info() << "\n";

		//For now I am moving both structures onto the orgin to compare them as I have failed to move one on to the other :-( TODO I could just also go backwards but for now this will do
		GeoTransformations* gt1 = tri1.getTransformation(tri1/*,orientation*/);
		GeoTransformations* gt2 = tri2.getTransformation(tri2/*, orientation*/);

		ss << "Transformation 1=\n" << gt1->info();
		ss << "Transformation 2=\n" << gt2->info();

		PDB1->getStructureVersion("A")->applyTransformation(gt1);
		PDB2->getStructureVersion("A")->applyTransformation(gt2);

		double val = calculateOneRMSD();
		ss << "RMSD Value = " << val;
		delete gt1;
		delete gt2;
		report = ss.str();
		return val;
	}
	else
	{
		LogFile::getInstance()->writeMessage("RMSD Opt, invalid tripod");
		return -1;
	}
}
double RMSD::calculateOneRMSD() // this may be iteratively called from an optimise function and needs to be fast
{			
	double rmsd = 0.0;
	for (unsigned int i = 0; i < _calphaPairs.size(); ++i)
	{//We are always using the shifted coordinates for this.
		GeoCoords aCoords = _calphaPairs[i].a1->shifted_coords;
		GeoCoords bCoords = _calphaPairs[i].a2->shifted_coords;
		double distance = 0.0;
		distance += pow((aCoords.x - bCoords.x), 2);
		distance += pow((aCoords.y - bCoords.y), 2);
		distance += pow((aCoords.z - bCoords.z), 2);
		rmsd += distance;
	}	
	return rmsd;
}

string RMSD::getAtomMatches()
{
	stringstream ss;	
	for (unsigned int i = 0; i < _calphaPairs.size(); ++i)	
		ss << _calphaPairs[i].a1->getDescription() << ":" << _calphaPairs[i].a2->getDescription() << "\n";;
	return ss.str();
}




