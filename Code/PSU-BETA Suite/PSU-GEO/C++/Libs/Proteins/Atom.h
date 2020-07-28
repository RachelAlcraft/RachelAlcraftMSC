#pragma once
#include "GeoCoords.h"
#include "GeoVector.h"
#include <string>
#include <vector>
#include <GeoTransformation.h>


using namespace std;
class Atom
{
public: //public struct
	//unique
	string dataId;
	int atomId = 0;
	string elementName;
	string elementType;
	string occupant;
	double occupancy;
	double bfactor;
	bool isAmino;
	bool bInsertion = false;
	
	//Parent
	string pdbCode;	
	string chainId;
	string aminoCode;
	int aminoId;
	
	//Geometric Info	
	GeoCoords coords;
	GeoCoords shifted_coords; // alternatively I could store a vector of shifts which could be animated - TODO
private:
	vector<Atom*> _bonds;
public:
	Atom(string,string);
	~Atom();
	void applyShift(double, double, double, bool);
	void printAtom();
	string getDescription();
	GeoVector vectorDifference(Atom*);
	double atomicDistance(Atom*,bool shifted);
	void applyTransformation(GeoTransformations* trans);
	vector<string> getObservation();

private:
	//string trim(string);

};

class AtomGeo
{
protected:
	string _aminoCode;	
	string _chain;
	int _aminoId;
	Atom* _A1;
	Atom* _A2;
	string _atomString;
	string _atomNoString;
	string _SS;
	string _geoDef;
	string _allAAs;
	string _aaNos;
	string _alias;
	string _geoType;


public:
	AtomGeo();
	string getChain() { return _chain; }
	string getAA() { return _aminoCode; }
	int getAminoId() { return _aminoId; }
	string getAtoms() { return _atomString; }
	string getAtomNos() { return _atomNoString; }
	string getGeoDef() { return _geoDef; }
	string getAACodes() { return _allAAs; }
	string getAminoNos() { return _aaNos; }
	string getSS() { return _SS; }
	string getAlias() { return _alias; }
	string getGeoType() { return _geoType; }
	virtual double getValue() = 0;
};

class AtomBond: public AtomGeo
{
public:	
	AtomBond(string aCode, string chain, int aId, string ss, Atom* a1, Atom* a2, string geo, string alias,string geotype);
	double getValue() override;
};

class AtomAngle : public AtomGeo
{	
	Atom* _A3;
public:
	AtomAngle(string aCode, string chain, int aId, string ss, Atom* a1, Atom* a2, Atom* a3, string geo, string alias,string geotype);
	double getValue() override;
	

};

class AtomTorsion: public AtomGeo
{	
	Atom* _A3;
	Atom* _A4;
public:
	AtomTorsion(string aCode, string chain, int aId, string ss, Atom* a1, Atom* a2, Atom* a3, Atom* a4, string geo, string alias,string geotype);
	double getValue() override;
	
};

