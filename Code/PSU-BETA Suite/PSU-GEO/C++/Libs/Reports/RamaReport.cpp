
#include "RamaReport.h"
#include <LogFile.h>
#include <ProteinManager.h>



void RamaReport::printReport(PDBFile* pdb, string occupant, string fileName)
{//produce data frame report for R reporting
	LogFile::getInstance()->writeMessage("Starting Torsion report");

	stringstream report;
	report << "Chain,AminoAcid,Id,Hydrophobocity,Hydropathy,Volume,Donicity,Chemical,Physio,Charge,Polar,Phi,Psi,Omega,Chi1,Chi2,Chi3,Chi4,Chi5,SS\n";
	map<string, Chain*> chains = ProteinManager::getInstance()->getChains(pdb->pdbCode, occupant);
	for (map<string, Chain*>::iterator iter = chains.begin(); iter != chains.end(); ++iter)
	{
		Chain* chain = iter->second;
		string chainid = iter->first;
		map<int, AminoAcid*> aminos = ProteinManager::getInstance()->getAminoAcids(pdb->pdbCode, occupant,chainid);
		for (map<int, AminoAcid*>::iterator iter = aminos.begin(); iter != aminos.end(); ++iter)
		{
			double phi = 0;
			double psi = 0;
			double omega = 0;
			double chi1 = 0;
			double chi2 = 0;
			double chi3 = 0;
			double chi4 = 0;
			double chi5 = 0;

			AminoAcid* aa = iter->second;
			BackboneTorsion* torsion = aa->getBackboneTorsion();
			SidechainTorsion* sidetorsion = aa->getSidechainTorsion();
			if (sidetorsion)
			{
				chi1 = sidetorsion->getChi1();
				chi2 = sidetorsion->getChi2();
				chi3 = sidetorsion->getChi3();
				chi4 = sidetorsion->getChi4();
				chi5 = sidetorsion->getChi5();
			}
			if (torsion)
			{
				double phi = torsion->getPhi();
				double psi = torsion->getPsi();
				double omega = torsion->getOmega();

				report << chainid << "," << aa->AminoCode << "," << aa->aminoId << ",";
				report << aa->Hydro << ",";
				report << aa->Hydropathy << ",";
				report << aa->Volume << ",";
				report << aa->Donicity << ",";
				report << aa->Chemical << ",";
				report << aa->Physio << ",";
				report << aa->Charge << ",";
				report << aa->Polar << ",";
				report << phi << "," << psi << "," << omega << ",";
				report << chi1 << "," << chi2 << "," << chi3 << "," << chi4 << "," << chi5 << "," << aa->getSS() << "\n";				
			}
		}
	}
	ofstream outfile(fileName);
	if (outfile.is_open())
	{
		outfile << report.str();
	}
}

/*string RamaReport::getSS(double phi, double psi)
{
	//Find the secondary structure on the ramachandran plot based on simple rules
	string ss = "";
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
	return ss;
}*/

