CREATE TABLE protein_set_b
(pdb_code CHAR(4) NOT NULL,
set_name VARCHAR(15)  NOT NULL,
status VARCHAR(15)  NOT NULL,
PRIMARY KEY (pdb_code,set_name),
FOREIGN KEY (pdb_code) REFERENCES protein_structure_b(pdb_code)
) ENGINE=InnoDB;

CREATE TABLE protein_set_c
(pdb_code CHAR(4) NOT NULL,
set_name VARCHAR(15)  NOT NULL,
status VARCHAR(15)  NOT NULL,
PRIMARY KEY (pdb_code,set_name)
) ENGINE=InnoDB;
