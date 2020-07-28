#include "Torsion.h"
#include "GeoVector.h"
#include "GeoPlane.h"
#include <LogFile.h>
/*
	Bonds are formed in the order
	C'-N-CA-C-N''-CA''
*/

Torsion::Torsion(string aa_name, int aa_id)
{
	aa = aa_name;
	id = aa_id;
	//_N = N;
	//_CA = CA;
	//_C = C;
}
BackboneTorsion::BackboneTorsion(string aa_name, int aa_id, vector<Atom*> atoms) :Torsion(aa_name, aa_id)
{
	if (atoms.size() == 6)
	{
		//Phi is Cp-N-CA-C
		_Phi.push_back(atoms[0]);
		_Phi.push_back(atoms[1]);
		_Phi.push_back(atoms[2]);
		_Phi.push_back(atoms[3]);
		//Psi is N-CA-C-NPP
		_Psi.push_back(atoms[1]);
		_Psi.push_back(atoms[2]);
		_Psi.push_back(atoms[3]);
		_Psi.push_back(atoms[4]);
		//Omega is CA-C-NPP-CAPP
		_Omega.push_back(atoms[2]);
		_Omega.push_back(atoms[3]);
		_Omega.push_back(atoms[4]);
		_Omega.push_back(atoms[5]);

	}
	else
	{
		//stringstream ss;
		//ss << "Error creating backbone torsion angles. AA=" << aa_name << " Atom=" << aa_id;
		//LogFile::getInstance()->writeMessage(ss.str());		
	}
	
}
SidechainTorsion::SidechainTorsion(string aa_name, int aa_id, vector<vector<Atom*>> atomslist) :Torsion(aa_name, aa_id)
{
	for (unsigned int i = 0; i < atomslist.size(); ++i)
	{
		vector<Atom*> atoms = atomslist[i];
		if (atoms.size() == 4)
		{//Not all amino acids will have all the Chis
			if (i == 0) //Not alanine or glycine
				_Chi1 = atoms;
			else if (i == 1)
				_Chi2 = atoms;
			else if (i == 2)
				_Chi3 = atoms;
			else if (i == 3)
				_Chi4 = atoms;
			else if (i == 4)//only arginine
				_Chi5 = atoms;
		}
		else
		{
			//stringstream ss;
			//ss << "Error creating sidechain torsion angles. AA=" << aa_name << " Atom=" << aa_id;
			//LogFile::getInstance()->writeMessage(ss.str());
		}
	}
}

double Torsion::getDihedralAngle(vector<Atom*> atoms)
{	//http://xiang-jun.blogspot.com/2009/10/how-to-calculate-torsion-angle.html
	if (atoms.size() == 4)
	{
		Atom* atmA = atoms[0];
		Atom* atmB = atoms[1];
		Atom* atmC = atoms[2];
		Atom* atmD = atoms[3];
		
		GeoVector ab = atmA->vectorDifference(atmB);
		GeoVector cb = atmC->vectorDifference(atmB);
		GeoVector cd = atmC->vectorDifference(atmD);

		GeoVector p = ab.getCrossProduct(cb);
		GeoVector q = cb.getCrossProduct(cd);

		double dot = p.getDotProduct(q);
		double magP = p.getMagnitude();
		double magQ = q.getMagnitude();

		double theta = acos(dot / (magP * magQ));

		//Now check the sign
		GeoVector r = p.getCrossProduct(q);
		double dotsign = r.getDotProduct(cb);
		if (dotsign > 0)
			theta *= -1;
		double theta_deg = (theta / 3.141592653589793238463) * 180;//convert to degrees 		
		//return round(theta_deg);		
		return theta_deg;
	}
	else
	{
		//For now I am just going to report 0 where there is not an angle, not ideal. Need to decide on this TODO.
		return 0;
	}
}

double BackboneTorsion::getPhi()
{//Cp:N:CA:C
	return getDihedralAngle(_Phi);
}
double BackboneTorsion::getPsi()
{//N:CA:C:Npp
	return getDihedralAngle(_Psi);
}
double BackboneTorsion::getOmega()
{//CA:C:Npp:CApp
	return getDihedralAngle(_Omega);
}
double SidechainTorsion::getChi1()
{//N:CA:C:AG1
	return getDihedralAngle(_Chi1);
}
double SidechainTorsion::getChi2()
{//CA:C:AG1:AD1		
	return getDihedralAngle(_Chi2);
}
double SidechainTorsion::getChi3()
{//CA:C:AG1:AD1		
	return getDihedralAngle(_Chi3);
}
double SidechainTorsion::getChi4()
{//CA:C:AG1:AD1		
	return getDihedralAngle(_Chi4);
}
double SidechainTorsion::getChi5()
{//CA:C:AG1:AD1		
	return getDihedralAngle(_Chi5);
}


