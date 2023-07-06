import csv
from db_connection import connect_db
import pandas as pd
import sys

from datetime import date, datetime, timedelta

today = date.today()
DATE = str(today).replace('-', '')

# PATH_1 = 'https://raw.githubusercontent.com/sermpezis/ai4netmon/main/data/aggregate_data/asn_aggregate_data_20221128.csv'
PATH_1 = './data/asn_aggregate_data_{}.csv'.format(DATE)

PATH_2 = './precalculated_bias.csv'

# categorical cause
ASRANK = './figures/Fig_Histogram_AS_rank_source.json'
ASCONT = './figures/Fig_Histogram_AS_rank_continent.json'
ASDBC1 = './figures/Fig_Histogram_ASDB_C1L1.json'
ASISPERS = './figures/Fig_Histogram_is_personal_AS.json'
PDBRATIO = './figures/Fig_Histogram_peeringDB_info_ratio.json'
PDBSCOPE = './figures/Fig_Histogram_peeringDB_info_scope.json'
PDBTRAFF = './figures/Fig_Histogram_peeringDB_info_traffic.json'
PDBTYPE = './figures/Fig_Histogram_peeringDB_info_type.json'
PDBPOLGEN = './figures/Fig_Histogram_peeringDB_policy_general.json'

# probes and rrcs
PROBES = './data/misc/RIPE_Atlas_probes_{}.json'.format(DATE)
RRC = './data/misc/RIPE_RIS_collectors_{}.json'.format(DATE)

# numerical cause
NUM_CAUSE = './platfCdf.json'


# ----------- LINSPACE DISTRIBUTIONS --------------
ASRANKlin = './figures_linspace/Fig_Histogram_AS_rank_source.json'
ASCONTlin = './figures_linspace/Fig_Histogram_AS_rank_continent.json'
ASDBC1lin = './figures_linspace/Fig_Histogram_ASDB_C1L1.json'
ASISPERSlin = './figures_linspace/Fig_Histogram_is_personal_AS.json'
PDBRATIOlin = './figures_linspace/Fig_Histogram_peeringDB_info_ratio.json'
PDBSCOPElin = './figures_linspace/Fig_Histogram_peeringDB_info_scope.json'
PDBTRAFFlin = './figures_linspace/Fig_Histogram_peeringDB_info_traffic.json'
PDBTYPElin = './figures_linspace/Fig_Histogram_peeringDB_info_type.json'
PDBPOLGENlin = './figures_linspace/Fig_Histogram_peeringDB_policy_general.json'

ASHEGElin = './figures_linspace/Fig_CDF_AS_hegemony.json'
ASCOSTlin = './figures_linspace/Fig_CDF_AS_rank_customer.json'
ASNUMADDlin = './figures_linspace/Fig_CDF_AS_rank_numberAddresses.json'
ASNUMASlin = './figures_linspace/Fig_CDF_AS_rank_numberAsns.json'
ASPREFlin = './figures_linspace/Fig_CDF_AS_rank_numberPrefixes.json'
ASPEERlin = './figures_linspace/Fig_CDF_AS_rank_peer.json'
ASPROVlin = './figures_linspace/Fig_CDF_AS_rank_provider.json'
ASTOTALlin = './figures_linspace/Fig_CDF_AS_rank_total.json'
CTIORlin = './figures_linspace/Fig_CDF_cti_origin.json'
CTITOPlin = './figures_linspace/Fig_CDF_cti_top.json'
FACCOUNTlin = './figures_linspace/Fig_CDF_peeringDB_fac_count.json'
IXCOUNTlin = './figures_linspace/Fig_CDF_peeringDB_ix_count.json'


# categorical_feats = [ASCONT, ASRANK, ASDBC1, ASISPERS, PDBRATIO, PDBSCOPE, PDBTRAFF, PDBTYPE, PDBPOLGEN]
# num_feats = [ASHEGE, ASCOST, ASNUMADD, ASNUMAS, ASPREF, ASPEER, ASPROV, ASTOTAL, CTIOR, CTITOP, FACCOUNT, IXCOUNT]

# agg_df = pd.read_csv(PATH_1, header=0)
# print(agg_df)

import json


def load_json(path):
    f = open(path)
    data = json.load(f)
    return data


ascont = load_json(ASCONT)
asrank = load_json(ASRANK)
asdbc1 = load_json(ASDBC1)
asispers = load_json(ASISPERS)
pdbratio = load_json(PDBRATIO)
pdbscope = load_json(PDBSCOPE)
pdbtraff = load_json(PDBTRAFF)
pdbtype = load_json(PDBTYPE)
pdbpolgen = load_json(PDBPOLGEN)
categorical_feats = [ascont, asrank, asdbc1, asispers, pdbratio, pdbscope, pdbtraff, pdbtype, pdbpolgen]

num_cause = load_json(NUM_CAUSE)

probes = load_json(PROBES)
rrc = load_json(RRC)
print(rrc)

ascontlin = load_json(ASCONTlin)
asranklin = load_json(ASRANKlin)
asdbc1lin = load_json(ASDBC1lin)
asisperslin = load_json(ASISPERSlin)
pdbratiolin = load_json(PDBRATIOlin)
pdbscopelin = load_json(PDBSCOPElin)
pdbtrafflin = load_json(PDBTRAFFlin)
pdbtypelin = load_json(PDBTYPElin)
pdbpolgenlin = load_json(PDBPOLGENlin)

ashegelin = load_json(ASHEGElin)
ascostlin = load_json(ASCOSTlin)
asnumaddlin = load_json(ASNUMADDlin)
asnumaslin = load_json(ASNUMASlin)
aspreflin = load_json(ASPREFlin)
aspeerlin = load_json(ASPEERlin)
asprovlin = load_json(ASPROVlin)
astotallin = load_json(ASTOTALlin)
ctiorlin = load_json(CTIORlin)
ctitoplin = load_json(CTITOPlin)
faccountlin = load_json(FACCOUNTlin)
ixcountlin = load_json(IXCOUNTlin)

feats_ = [ascontlin, asranklin, asdbc1lin, asisperslin, pdbratiolin, pdbscopelin, pdbtrafflin, pdbtypelin, pdbpolgenlin,
          ashegelin, ascostlin, asnumaddlin,
          asnumaslin, aspreflin, aspeerlin, asprovlin, astotallin, ctiorlin, ctitoplin, faccountlin, ixcountlin]


def db_insertion_aggdf(path):
    db = connect_db()
    # set collection
    db.aggregated_dataframe.drop()

    # ------- FOR PANDAS DF ---------
    agg_df = pd.read_csv(path, header=0) # aggregated dataframe does not need index_col, in order to save ASN too

    header = list(agg_df)
    # print(header)
    csvfile = open(path, 'r')
    reader = csv.DictReader(csvfile)

    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]

        # print(row)
        db.aggregated_dataframe.insert_one(row)
    print("Agg df inserted!")


def db_insertion_bias(path):
    db = connect_db()
    # set collection
    db.precalc.drop()

    # ------- FOR PANDAS DF ---------
    agg_df = pd.read_csv(path, header=0, index_col=0) # use for all the other collections

    header = list(agg_df)
    # print(header)
    csvfile = open(path, 'r')
    reader = csv.DictReader(csvfile)

    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]

        # print(row)
        db.precalc.insert_one(row)


def db_insertion_categ_cause():
    db = connect_db()
    # set collection
    db.histjsons.drop()

    # ------- FOR JSONS ---------
    for feat in categorical_feats:
        db.histjsons.insert_one(feat)


def db_insertion_num_cause():
    db = connect_db()
    # set collection
    db.cdfjsons.drop()

    # ------- FOR JSONS ---------
    db.cdfjsons.insert_one(num_cause)


def db_insertion_probes():
    db = connect_db()
    db.probes.drop()

    db.probes.insert_many(probes)


def db_insertion_rrc():
    db = connect_db()
    db.rrc.drop()

    db.rrc.insert_many(rrc)


def db_insertion_distributions():
    db = connect_db()
    db.distributions.drop()
    for feat in feats_:
        db.distributions.insert_one(feat)

# db_insertion(PATH_4)

# db_insertion(PATH_2)

# db_insertion_aggdf(PATH_1)

# try:
#     db_insertion_aggdf(PATH_1)
# except Exception:
#     print('An error occurred in inserting agg df!')
# else:
#     print("Agg df inserted!")

try:
    db_insertion_bias(PATH_2)
except Exception:
    print('An error occurred in inserting precalc biases!')
else:
    print("Biases inserted!")

try:
    db_insertion_categ_cause()
except Exception:
    print('An error occurred in inserting categorical bias causes!')
else:
    print("Categorical bias causes inserted!")

try:
    db_insertion_num_cause()
except Exception:
    print('An error occurred in inserting numerical bias causes!')
else:
    print("Numerical bias causes inserted!")

try:
    db_insertion_distributions()
except Exception:
    print('An error occurred in inserting distributions!')
else:
    print("Distributions inserted!")

try:
    db_insertion_probes()
except Exception:
    print('An error occurred in inserting Atlas probes!')
else:
    print("Atlas probes inserted!")

try:
    db_insertion_rrc()
except Exception:
    print('An error occurred in inserting RRCs!')
else:
    print("RRCs inserted!")
# db_insertion_rrc()
