CREATE TABLE protein_structure_c
(pdb_code CHAR(4) NOT NULL,
resolution DECIMAL(7,3) NOT NULL,
seq VARCHAR(2000) NOT NULL,
struct_class VARCHAR(50) NOT NULL,
complex BOOL NOT NULL,
rvalue DECIMAL(20,3) NOT NULL,
rfree DECIMAL(20,3) NOT NULL,
occupancy BOOL NOT NULL,
bfactor DECIMAL(10,3) NOT NULL,
hydrogens BOOL NOT NULL,
struct_fact  BOOL NOT NULL,
chains VARCHAR(15) NOT NULL,
residues SMALLINT NOT NULL,
nucleotides SMALLINT NOT NULL,
deposit_date DATETIME NOT NULL,
refinement VARCHAR(50) NOT NULL,
exp_method VARCHAR(3) DEFAULT 'XR' NOT NULL,
institution VARCHAR(200) DEFAULT 'Unknown' NOT NULL,
PRIMARY KEY (pdb_code)
) ENGINE=InnoDB;



