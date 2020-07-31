CREATE TABLE geo_calcs_v1
(amino_code CHAR(3) NOT NULL,
calc_type VARCHAR(15)  NOT NULL,
calc_atoms VARCHAR(50)  NOT NULL,
calc_alias VARCHAR(50)  NOT NULL,
PRIMARY KEY (amino_code,calc_alias)
) ENGINE=InnoDB;

CREATE TABLE protein_set_c
(pdb_code CHAR(4) NOT NULL,
set_name VARCHAR(15)  NOT NULL,
status VARCHAR(15)  NOT NULL,
PRIMARY KEY (pdb_code,set_name)
) ENGINE=InnoDB;
