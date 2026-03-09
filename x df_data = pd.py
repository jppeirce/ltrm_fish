x df_data = pd.read_csv("ltrm_fish_D_p4813_aa1_aa3_all.csv", low_memory=False)
x df_data['year'] = pd.to_datetime(df_data['sdate']).dt.year
x df_data = df_data[df_data['fishcode'].notna()].reset_index(drop=True)
x df_data = df_data[(~df_data['fishcode'].str.startswith('U-')) & (~df_data['fishcode'].isin(['NFSH', 'UNID']))].reset_index(drop=True)
x hybrid_fish = ['BCWC', 'BGLE', 'BGOS', 'BGRS', 'BGWM', 'CCGF', 'GSBG', 'GSPS', 'GSRS', 'GSWM', 'GSOS', 'LNST', 'OSLE', 'PSBG', 'PSOS', 'PSWM', 'SBWB', 'SCBS', 'SGWE', 'SNPD', 'WPYB']  
x df_data = df_data[~df_data['fishcode'].isin(hybrid_fish)].reset_index(drop=True)
x df = df_data[df_data['period'] == 3].reset_index(drop=True)
x keep_cols =['utm_e', 'utm_n', 'barcode', 'year', 'pool', 'fishcode', 'AQUA_DESC']
x df = df[keep_cols].reset_index(drop=True)

agg_df = df.groupby(['barcode']).agg(
    utm_e=('utm_e', 'median'),
    utm_n=('utm_n', 'median'),
    year=('year', lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]),
    mode_pool=('pool', lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]),
    fish_codes=('fishcode', lambda x: list(x)), # all fish observed on that date
    mode_aqua_desc=('AQUA_DESC', lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0])
).reset_index()

unique_fish = set([item for sublist in agg_df['fish_codes'] for item in sublist])
fish_df = pd.DataFrame({fish: agg_df['fish_codes'].apply(lambda x: fish in x) for fish in unique_fish})
agg_df = pd.concat([agg_df, fish_df], axis=1)   
agg_df.drop(columns=['fish_codes'], inplace=True)
agg_df['mode_pool'] = agg_df.apply(assign_pool, axis=1)

min_occurrence = len(fish_df) * 0.05

# Find fish species that occur in at least 5% of barcodes
species_counts = fish_df.sum(axis=0)  # sum down columns (each column is a species)
common_species = species_counts[species_counts >= min_occurrence].index.tolist()

# Filter fish_df to keep only common species
fish_df_filtered = fish_df[common_species].copy()

fish_df_filtered.to_csv('pandas/fish_df.csv', index=False)