import numpy as np
import pandas as pd
import json
import random
from bias_utils import bias_score_dataframe, get_feature_type
from generate_distribution_plots import plot_all
from data_aggregation_tools import load_aggregated_dataframe

## datasets
df = load_aggregated_dataframe()

FIG_RADAR_SAVENAME_FORMAT = './figures/fig_radar_{}.png'
# BIAS_CSV_FNAME = './data/bias_values_ris_rv_bgptools.csv'
BIAS_CSV_FNAME = './data/bias_values_bgptools.csv'
# BIAS_CSV_FNAME = './data/bias_values_periscope.csv'

SAVE_PLOTS_DISTRIBUTION_FNAME_FORMAT = './figures/Fig_{}_{}'
SAVE_PLOTS_DISTRIBUTION_all_FNAME_FORMAT = './figures/Fig_{}_{}_all_lists'

OMIT_STUBS = False

# select features for visualization
FEATURES = get_feature_type(feature='numerical', all_features=True)
# print(FEATURES)
# FEATURES = list(FEATURE_NAMES_DICT.keys())
# print(FEATURES)
# FEATURES = ['AS_hegemony']
# FEATURES = ['AS_rank_source', 'AS_hegemony', 'cti_origin', 'AS_rank_continent']

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
# print(df['AS_hegemony'].describe())
# print(df['AS_hegemony'].info())


df['is_personal_AS'].fillna(0, inplace=True)
# if OMIT_STUBS:
#     df = df[df['AS_rel_degree']>1]
#     FIG_RADAR_SAVENAME_FORMAT = FIG_RADAR_SAVENAME_FORMAT_NO_STUBS
#     BIAS_CSV_FNAME = BIAS_CSV_FNAME_NO_STUBS
df['ASDB_C1L1'] = df['ASDB_C1L1'].replace(asdb_dict)

# define sets of interest
network_sets_dict = dict()
network_sets_dict['all'] = df

# print(network_sets_dict['broken lists responsible'])
# net_set_dict_names = ['RIPE Atlas (all)', 'RIPE RIS (all)', 'RouteViews (all)', 'RIPE RIS & RouteViews', 'bgptools (all)']
net_set_dict_names = ['Atlas', 'RIS', 'RouteViews', 'RIS&RouteViews', 'bgptools']

# all_d = {'RIPE Atlas': {}, 'RIPE RIS': {}, 'RouteViews': {}, 'BGPtools': {}}
# all_d = {}
all_d = []
# all_dict = {}
platf_list_keys = ['RIPE Atlas', 'RIPE RIS', 'RouteViews', 'RIS&RouteViews', 'BGPtools']

for platf in net_set_dict_names:
    if platf == 'RIS':
        network_sets_dict[platf] = df.loc[(df['is_ris_peer_v4'] > 0) | (df['is_ris_peer_v6'] > 0)]
    elif platf == 'Atlas':
        network_sets_dict[platf] = df.loc[(df['nb_atlas_probes_v4'] > 0) | (df['nb_atlas_probes_v6'] > 0)]
    elif platf == 'RouteViews':
        network_sets_dict[platf] = df.loc[df['is_routeviews_peer'] > 0]
    elif platf == 'RIS&RouteViews':
        df_mon = df.loc[(df['is_ris_peer_v4'] > 0) | (df['is_ris_peer_v6'] > 0) | (df['is_routeviews_peer'] > 0)]
    elif platf == 'bgptools':
        network_sets_dict[platf] = df.loc[(df['is_bgptools_peer_v4'] > 0) | (df['is_bgptools_peer_v6'] > 0)]

    # calculate bias dataframes
    network_sets_dict_for_bias = {k: v[FEATURES] for k, v in network_sets_dict.items() if k != 'all'}
    #
    params = {'method': 'kl_divergence', 'bins': 10, 'alpha': 0.01}
    # params={'bins':20, 'alpha':0.01}

    from itertools import pairwise

    ### find cause of bias in numerical features and export json ###

    bias_df, p, q, bins = bias_score_dataframe(df[FEATURES], network_sets_dict_for_bias, **params)
    # print(list(bias_df.index))

    pairbins = []
    print(bins)
    bins1 = []
    # save feats with really small or negative numbers in another list
    bins1.append(bins[9])
    bins1.append(bins[-1])
    bins1.append(bins[-2])
    # delete from original list to process it with map (int) correctly
    del bins[9] # delete
    del bins[-1]
    del bins[-1]
    # print()

    bins = np.ceil(np.exp(bins))
    # print(bins)
    # df =
    # bins = bins
    # for bin in bins:
    #     bin = list(map(int, bin))

    # print("bins", bins)
    bins = np.vstack([bins,bins1])

    for b in bins:
        pairbins.append(list(pairwise(b)))

    list_of_keys = ['AS_rank_numberAsns', 'AS_rank_numberPrefixes', 'AS_rank_numberAddresses', 'AS_rank_total', 'AS_rank_customer', 'AS_rank_peer', 'AS_rank_provider', 'peeringDB_ix_count', 'peeringDB_fac_count', 'peeringDB_info_prefixes4', 'peeringDB_info_prefixes6', 'nb_atlas_probes_v4', 'nb_atlas_probes_v6', 'AS_hegemony', 'cti_origin', 'cti_top']

    all_dist = {list(list_of_keys)[i]: p[i] for i in range(len(list(list_of_keys)))}
    platf_dist = {list(list_of_keys)[i]: q[i] for i in range(len(list(list_of_keys)))}

    # pairbins1 = {list(bias_df.index)[i]: pairbins[i] for i in range(len(list(bias_df.index)))}
    pairbins1 = {list(list_of_keys)[i]: pairbins[i] for i in range(len(list(list_of_keys)))}
    diff = {key: (np.subtract(platf_dist[key], all_dist.get(key, 0))).tolist() for key in platf_dist}
    diff = {x: [str(round(y * 100, 4)) + '%' for y in diff[x]] for x in diff}


    def combine_dictionaries(dict1, dict2):
        result = {}
        for key in dict1:
            if key in dict2:
                value1 = dict1[key]
                value2 = dict2[key]
                combined_values = [(value1[i], value2[i]) for i in range(min(len(value1), len(value2)))]
                # combined_values = {"-".join([str(j) for j in value2[i]]): value1[i] for i in range(min(len(value1), len(value2)))}
                result[key] = combined_values
        return result


    d = combine_dictionaries(diff, pairbins1)
    # print("d hereeeeeeee", d)
    all_d.append(d)
    # all_d[platf] = d

print("all d", all_d)
all_dict = {list(platf_list_keys)[i]: all_d[i] for i in range(len(list(platf_list_keys)))}

# print(all_dict)
# print(d['AS_rank_numberAsns'][0][1])
#
with open("platfCdf.json", "w") as outfile:
    jsonn.dump(all_dict, outfile)
