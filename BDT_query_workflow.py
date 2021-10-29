#
# This will automatically perform a search specific queries through the entire ArXiv plaintext library
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from Miner_base import *

# Adjust wordlist prior to initialising Mine()
wordlist = ['BDT','boosted\n\n\ndecision tree','boosted decision\n\n\ntree',
            'boosted\n\n\nregression tree','boosted regression\n\n\ntree','boosted decision tree',
            'boosted tree', 'BRT', 'boosted regression tree']
Mine = Mine(wordlist=wordlist)

# Set Directory of ArXiv plaintext library
Mine.load_ids_from_dir(path='/home/preid/projects/def-doneil/preid/ArXiv/ArXiv_plaintext/')

# Run the Query
Mine.query_local_arxiv_lib(path='/home/preid/projects/def-doneil/preid/ArXiv/ArXiv_plaintext/', to_csv=True)