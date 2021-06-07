'''
this is for testing out the RDKit library
'''

import sys
#sys.path.append('/usr/local/lib/python3.7/site-packages/')
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit import DataStructs
import numpy as np
import jupyter


smiles = 'COC(=O)c1c[nH]c2cc(OC(C)C)c(OC(C)C)cc2c1=O'

# convert smiles to rdkit mol 
mol = Chem.MolFromSmiles(smiles)
print(mol)

# convert rdkit mol to smiles
smi = Chem.MolToSmiles(mol)

# covert mol to inchikey
Chem.MolToInchiKey(mol)

# convert molecule to coordinative representation (which can be stored in .sdf file)
mol_block = Chem.MolToMolBlock(mol)
print(mol_block)

# molecule file formats: 
# .csv file that includes a column of SMILES. See PandasTools section.
# open .smi file (smiles list) and save to array
try :
    file = 'filename.smi'

    with open(file, "r") as f:
        smiles = []
        for line in f:
            smiles.append(line.split('\n')[0])
    print('number of smiles:', len(smiles))
except :
    pass

# draw mol in jupyter/ interactive window
smiles = [
    'N#CC(OC1OC(COC2OC(CO)C(O)C(O)C2O)C(O)C(O)C1O)c1ccccc1',
    'c1ccc2c(c1)ccc1c2ccc2c3ccccc3ccc21',
    'C=C(C)C1Cc2c(ccc3c2OC2COc4cc(OC)c(OC)cc4C2C3=O)O1',
    'ClC(Cl)=C(c1ccc(Cl)cc1)c1ccc(Cl)cc1'
]

mols = [Chem.MolFromSmiles(smi) for smi in smiles]
Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(200, 200))

# 2do
# Looping over Atoms and Bonds
# Modifying molecule
# Working with 3D Molecules
# Substructure Searching
# Chemical Reactions