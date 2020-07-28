#pragma once
/* 
SINGLETON pattern datamanager class
This is a kind of runtime relational database
The class also manages the loading of some config data
The important thing about this class it manages all the pointes and is the responsible object for all pointer deletion
Pointers are created and deleted just once in the program not really dynamically
*/
#include <string>
#include <map>
#include <set>
#include <vector>
#include <AminoAcid.h>
#include <Chain.h>
#include <Atom.h>
#include <PDBFile.h>

using namespace std;
class ProteinManager
{
private:
	static ProteinManager* instance;
	ProteinManager();
	//string _configPath;

	//DATA HIERARCHY//////////////////////////////////////////
	//Amino acids have general data
	map<string, string> _aa_generaldata; // 3 letter AA code vs a long string of data to parse into the aa init
	
	//Amino acids have geometric preferences

	//Force field

	
	//PROTEIN HIERARCHY////////////////////////////////////
	//a pdb file has
		//chains
			//which have amino acids
				//which have atoms
	//There are also bonds, torsions angles and angles

	//PDBFile has chains
	map<string,PDBFile*> _pdbfiles;
	//map<string, vector<Chain*>> _chains; //id = PDBCODE 		
	//Chains have amino acids
	//map<string, vector<AminoAcid*>> _aminos; //id = PDBCODE_chainNo 
	//amino acids have atoms (which may be shifted in optimisation algorithms)
	//map<string, vector<Atom*>> _atoms; //id = PDBCODE_chainNo_aminoNo

	//amino acids have bonds

	//amino acids have angles
	
	//amino acids have torsion phi, psi, omega and chi angles

	//Amino acids have improper bonds
	
	//Atoms are involved in hydrogen bonds

public:
	static ProteinManager* getInstance();
	~ProteinManager(); //responsible for pdbs
	void deletePdbs();//in case we are just examining pdbs and don;t want loads
	void createAminoAcidData(string filename);
	vector<string> getAminoData(string aminoCode);
	void addAtom(string pdbCode, string occupant, string chainId, int aminoId, Atom* atm);
	PDBFile* getOrAddPDBFile(string pdbCode, string filename);
	AminoAcid* getOrAddAminoAcid(string pdbCode, string occupant, string chainId, int aminoId, string amino_code, int& structure_id);
	NucleicAcid* getOrAddNucleicAcid(string pdbCode, string occupant, string chainId, int aminoId, string amino_code, int& structure_id, int& residuenum);
	Chain* getOrAddChain(string pdbCode, string occupant, string chainId);
	map<string, Chain*> getChains(string pdbCode, string occupant);
	map<int, AminoAcid*> getAminoAcids(string pdbCode, string occupant, string chainId);
	vector<Atom*> getCAlphas(string pdbCode, string occupant, string chainId, string atom);
	vector<Atom*> getCAlphas(string pdbCode, string occupant, string atom);
	vector<Atom*>  getAtoms(string pdbCode, string occupant);
	map<int,Atom*>  getAtomsMap(string pdbCode, string occupant);
	vector<AtomBond>  getAtomBonds(string pdbCode, string occupant);
	vector<AtomAngle>  getAtomAngles(string pdbCode, string occupant);
	vector<AtomTorsion>  getAtomTorsions(string pdbCode, string occupant);
	bool hasOccupancy(string pdbCode, string occupant);
	vector<string> occupantList(string pdbCode);
	double maxBFactor(string pdbCode, string occupant);
	bool hasHydrogens(string pdbCode, string occupant);
	bool isAminoAcid(string code);
	bool isNucleicAcid(string code);

	

private:
	//vector<string> stringToVector(string input, string delim);






};

