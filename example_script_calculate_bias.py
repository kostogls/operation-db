import numpy as np
import pandas as pd
import json
import random
from matplotlib import pyplot as plt
from bias_utils import get_features_dict_for_visualizations, bias_score_dataframe, get_bias_of_monitor_set
from generate_distribution_plots import save_all_dist_jsons
from data_aggregation_tools import load_aggregated_dataframe
from collections import defaultdict
from data_collectors import get_ripe_ris_data

## datasets
# AGGREGATE_DATA_FNAME = './data/asn_aggregate_data_20230531.csv'
df = load_aggregated_dataframe()
# select features for visualization
FEATURE_NAMES_DICT = get_features_dict_for_visualizations()
FEATURES = list(FEATURE_NAMES_DICT.keys())

asdb_dict = {
    'Computer and Information Technology': 'ICT',
    'Retail Stores, Wholesale, and E-commerce Sites': 'Retail & E-commerce',
    'Finance and Insurance': 'Finance',
    'Service': 'Service',
    'Education and Research': 'Edu. & Research',
    'Media, Publishing, and Broadcasting': 'Media',
    'Manufacturing': 'Manufacturing',
    'Government and Public Administration': 'Gov. & Public',
    'Construction and Real Estate': 'Real Estate',
    'Other': 'Other',
    'Community Groups and Nonprofits': 'Nonprofit',
    'Health Care Services': 'Health',
    'Freight, Shipment, and Postal Services': 'Shipment & postal',
    'Museums, Libraries, and Entertainment': 'Entertainment',
    'Travel and Accommodation': 'Travel',
    'Agriculture, Mining, and Refineries (Farming, Greenhouses, Mining, Forestry, and Animal Farming)': 'Agro, Mining, etc.',
    'Utilities (Excluding Internet Service)': 'Utilities'
}

## load data
# df = pd.read_csv(AGGREGATE_DATA_FNAME, header=0, index_col=0)
df['is_personal_AS'].fillna(0, inplace=True)
# if OMIT_STUBS:
#     df = df[df['AS_rel_degree']>1]
#     FIG_RADAR_SAVENAME_FORMAT = FIG_RADAR_SAVENAME_FORMAT_NO_STUBS
#     BIAS_CSV_FNAME = BIAS_CSV_FNAME_NO_STUBS
df['ASDB_C1L1'] = df['ASDB_C1L1'].replace(asdb_dict)


# define sets of interest
network_sets_dict = dict()
network_sets_dict['all'] = df
network_sets_dict['RIPE RIS (all)'] = df.loc[(df['is_ris_peer_v4']>0) | (df['is_ris_peer_v6']>0)]
network_sets_dict['RIPE RIS (v4)'] = df.loc[df['is_ris_peer_v4']>0]
network_sets_dict['RIPE RIS (v6)'] = df.loc[df['is_ris_peer_v6']>0]
network_sets_dict['RIPE Atlas (all)'] = df.loc[(df['nb_atlas_probes_v4']>0) | (df['nb_atlas_probes_v6']>0)]
network_sets_dict['RIPE Atlas (v4)'] = df.loc[df['nb_atlas_probes_v4']>0]
network_sets_dict['RIPE Atlas (v6)'] = df.loc[df['nb_atlas_probes_v6']>0]
network_sets_dict['RouteViews (all)'] = df.loc[df['is_routeviews_peer']>0]
network_sets_dict['bgptools (all)'] = df.loc[(df['is_bgptools_peer_v4']>0) | (df['is_bgptools_peer_v6']>0)]
network_sets_dict['bgptools (v4)'] = df.loc[(df['is_bgptools_peer_v4']>0)]
network_sets_dict['bgptools (v6)'] = df.loc[(df['is_bgptools_peer_v6']>0)]
network_sets_dict['RIPE RIS + RouteViews (all)']= df.loc[(df['is_ris_peer_v4']>0) | (df['is_ris_peer_v6']>0) | (df['is_routeviews_peer']>0)]

ris_peer_ip2asn, ris_peer_ip2rrc = get_ripe_ris_data()
rrc2asn_dict = defaultdict(list)
for ip, rrc in ris_peer_ip2rrc.items():
    rrc2asn_dict[rrc].append( ris_peer_ip2asn[ip] )

# calculate biases
bias_df = get_bias_of_monitor_set(df=df, imp='RIPE RIS')
for rrc, rrc_asns in rrc2asn_dict.items():
    bias_df_rrc = get_bias_of_monitor_set(df=df, imp=rrc, monitor_list=rrc_asns, params=None)
    bias_df = pd.concat([bias_df, bias_df_rrc], axis=1)

# print(bias_df)
bias_df.drop(['RIPE RIS'], axis=1, inplace=True)

# print(network_sets_dict['broken lists responsible'])

# calculate bias dataframes
network_sets_dict_for_bias = {k:v[FEATURES] for k,v in network_sets_dict.items() if k != 'all'}
#
#
params = {'method':'kl_divergence', 'bins':10, 'alpha':0.01}
bias_df2, _, _, _ = bias_score_dataframe(df[FEATURES], network_sets_dict_for_bias, **params)
# # print biases & save to csv
# print('Bias per monitor set (columns) and per feature (rows)')
print_df = bias_df2[['RIPE Atlas (all)','RIPE RIS (all)', 'RouteViews (all)', 'RIPE RIS + RouteViews (all)',
                    'bgptools (all)']].copy()

# print_df.index = [n.replace('\n','') for n in FEATURE_NAMES_DICT.values()]
# print(print_df)
print_df.rename(columns={'RIPE Atlas (all)': 'Atlas', 'RIPE RIS (all)': 'RIS',
                    'RouteViews (all)': 'RouteViews','RIPE RIS + RouteViews (all)': 'RIS&RouteViews', 'bgptools (all)': 'bgptools'}, inplace=True)

f_df = pd.concat([bias_df, print_df], axis=1)
# print(f_df)
tr_df = f_df.T
tr_df['list_name'] = tr_df.index
tr_df.columns = ['RIR region', 'Location (country)', 'Location (continent)', 'Customer cone (#ASNs)', 'Customer cone (#prefixes)',
                 'Customer cone (#addresses)', 'AS hegemony', 'Country influence (CTI origin)', 'Country influence (CTI top)', '#neighbors (total)', '#neighbors (peers)',
                 '#neighbors (customers)', '#neighbors (providers)', '#IXPs (PeeringDB)', '#facilities (PeeringDB)',
                 'Peering policy (PeeringDB)', 'Network type (PeeringDB)', 'Traffic ratio (PeeringDB)', 'Traffic volume (PeeringDB)',
                 'Scope (PeeringDB)', 'Personal ASN', 'ASDB C1L1', 'ASDB C1L2', 'list_name']

tr_df.to_csv('precalculated_bias.csv', header=True, index=True)

# print(df.dtypes)
SAVE_PLOTS_DISTRIBUTION_FNAME_FORMAT = './figures/Fig_{}_{}'
SAVE_PLOTS_DISTRIBUTION_LIN_FNAME_FORMAT = './figures_linspace/Fig_{}_{}'

network_sets_dict_plots = {'All ASes': network_sets_dict['all'],
                           'RIPE Atlas': network_sets_dict['RIPE Atlas (all)'],
                           'RIPE RIS': network_sets_dict['RIPE RIS (all)'],
                           'RouteViews': network_sets_dict['RouteViews (all)'],
                           'RIPE RIS + RouteViews': network_sets_dict['RIPE RIS + RouteViews (all)'],
                           'BGPtools': network_sets_dict['bgptools (all)']}

# print(network_sets_dict_plots)
save_all_dist_jsons(network_sets_dict_plots, SAVE_PLOTS_DISTRIBUTION_FNAME_FORMAT, linspace=False)

save_all_dist_jsons(network_sets_dict_plots, SAVE_PLOTS_DISTRIBUTION_LIN_FNAME_FORMAT, linspace=True)
