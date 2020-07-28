#pragma once
#include "Atom.h"

class Torsion
{//FOR NOW insist that a torsion has all of the possible atoms
	//Bonds are formed in the order
	//C'-N-CA-C-N''-CA''
public:
	int id;
	string aa;
protected:
	
public: //methods
	Torsion(string, int);
	static double getDihedralAngle(vector<Atom*>);

};

class BackboneTorsion : public Torsion
{
protected:
	vector<Atom*> _Phi;
	vector<Atom*> _Psi;
	vector<Atom*> _Omega;
public:
	BackboneTorsion(string, int,vector<Atom*>);
	double getPhi();
	double getPsi();
	double getOmega();

};

class SidechainTorsion : public Torsion
{
protected:
	vector<Atom*> _Chi1;
	vector<Atom*> _Chi2;
	vector<Atom*> _Chi3;
	vector<Atom*> _Chi4;
	vector<Atom*> _Chi5;

public:
	SidechainTorsion(string, int, vector<vector<Atom*>>);
	double getChi1();
	double getChi2();
	double getChi3();
	double getChi4();
	double getChi5();

};

