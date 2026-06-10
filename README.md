# Spatial and Temporal Changes in Fish Assemblages of the Upper Mississippi River

Code supporting the manuscript: **"Spatial and Temporal Changes in Fish Assemblages of the Upper Mississippi River"**

Authors: James Peirce[1], David Elzinga[1,2], Richard A. Erickson[3], Daniel Gibson-Reinemer[3], Danelle M. Larson[3], Markus Mika[4], Gregory Sandland[4], David Schumann[4], Kristen L. Bouska[3]

[1] University of Wisconsin-La Crosse, Department of Mathematics and Statistics, La Crosse, WI 54601, USA 

[2] Current affiliation: Dairyland Power Cooperative, La Crosse, WI 54601 

[3] U.S. Geological Survey, Upper Midwest Environmental Sciences Center, 2630 Fanta Reed Road, La Crosse, WI 54603, USA 

[4] University of Wisconsin-La Crosse, Department of Biology, La Crosse, WI 54601, USA 
---

## Abstract

Freshwater fish assemblages reflect the interplay between environmental conditions, habitat suitability, and species interactions. In large rivers, long-term changes in flow, water quality, and habitat can alter species co-occurrence and assemblage structure over time. The Upper Mississippi River (UMR) has experienced substantial ecological change, including habitat modifications, improvements in water quality, and introductions of invasive species, that have likely influenced the composition and distribution of native fish communities. We used more than three decades of standardized monitoring data collected across four study reaches within a 400-kilometer section of the UMR to quantify fish assemblages during autumn, a season that reflects habitat conditions prior to overwintering. We applied hierarchical clustering to long-term abundance data to identify meaningful patterns in fish species co-occurrence. Clustering revealed six statistically and ecologically meaningful fish assemblages with distinct spatial distributions and temporal trends over the 32-year record, indicating system-wide shifts in community structure. Notable regional shifts included a decline in lotic-adapted assemblages in most reaches alongside an increase in more diverse and functionally complex communities, consistent with documented improvements in water quality and aquatic vegetation recovery. This clustering approach offers a practical framework for linking assemblage dynamics to habitat changes and management actions, supporting targeted restoration and conservation strategies aimed at sustaining biodiversity and recreational fisheries in one of North America's largest rivers. 

## Overview

This analysis uses Long Term Resource Monitoring (LTRM) electrofishing data from Pools 4, 8, and 13 of the Upper Mississippi River to identify fish assemblage clusters and track their spatial and temporal dynamics from 1993–2024. The workflow consists of three sequential Jupyter notebooks.

---

## Data

**`ltrm_fish_D_p4813_aa1_aa3_all.csv`** — Source data from the USGS Upper Midwest Environmental Sciences Center LTRM fish monitoring program. Contains daytime electrofishing samples from Pools 4, 8, and 13, spatially joined with Aquatic Areas I and III datasets.

- Data dictionary: https://www.umesc.usgs.gov/cgi-bin/ltrmp/fish/fish_meta.pl
- Each row is an individual fish observation identified by `barcode` (sample event)
- Key fields: `barcode`, `fishcode`, `pool`, `sdate`, `utm_e`, `utm_n`, `AQUA_DESC`, `AQUA_CODE3`, `period`

---

## Notebooks

### `1data_wrangling.ipynb` — Data Preparation

Filters and reformats raw LTRM data into a site × species presence/absence matrix.

**Filtering steps:**
1. Removes records with missing fish codes, unidentified species (`U-*`, `UNID`), and no-fish records (`NFSH`)
2. Removes hybrid fish codes (21 hybrid codes excluded)
3. Removes Pool 8 samples from 2020 (COVID-19 restricted sampling)
4. Restricts to Period 3 (daytime electrofishing protocol)
5. Retains only 7 columns relevant to the analysis

**Aggregation:**
- Groups by `barcode` (sample event) to create one row per sampling occasion
- Expands fish species into binary presence/absence columns (93 species initially)
- Splits Pool 4 into Upper Pool 4 (utm_n > 4,925,000) and Lower Pool 4

**Species filtering:**
- Removes species occurring in fewer than 5% of samples
- Final dataset: 2,388 samples × 41 common species

**Outputs** (saved to `pandas/`):
| File | Contents |
|------|----------|
| `df_filtered.csv` | Filtered long-format data (Period 3 only) |
| `df_data.csv` | All periods after initial filtering |
| `agg_df.csv` | Aggregated site × metadata matrix (2,388 × 99) |
| `fish_df.csv` | Species presence/absence matrix (2,388 × 41 common species) |

---

### `2cluster_analysis.ipynb` — Hierarchical Cluster Analysis

Applies agglomerative hierarchical clustering using Jaccard distance to group sampling events by fish assemblage similarity.

**Distance metric:** Jaccard dissimilarity (presence/absence data; consistent with prior ecological analyses on these data)

**Linkage method:** Average linkage (UPGMA)

**Threshold selection** (`select_clustering_threshold` function):
A custom bootstrap-based method selects the Jaccard distance threshold for cutting the dendrogram. For each candidate threshold, the function:
- Computes full-data cluster partitions across a grid of 100 thresholds (0.60–0.90)
- Runs 1,000 bootstrap subsamples (80% of data, without replacement) and computes Adjusted Rand Index (ARI) against full-data labels
- Calculates cluster instability (1 − ARI), partition volatility (Variation of Information between adjacent thresholds), and size penalties for small clusters
- Applies hard constraints: no clusters larger than 1,000, no more than 10 clusters smaller than 90 samples
- Selects the threshold minimizing a weighted composite score

**Selected threshold:** 0.697 (mean bootstrap ARI = 0.44 ± 0.065)

**Cluster numbering:** Clusters are renumbered 1–*n* in descending order of size (Cluster 1 = largest).

**Outputs** (saved to `pandas/`):
| File | Contents |
|------|----------|
| `agg_df_cluster1.csv` | Site metadata with cluster assignments |
| `fish_df_cluster1.csv` | Species presence/absence with cluster assignments |

---

### `3cluster_visualization.ipynb` — Cluster Visualization and Temporal Analysis

Generates all figures for the manuscript. Restricts analysis to the 6 ecologically interpretable clusters with ≥ 40 samples (80.6% of sampling events retained).

**Species composition heatmap**
- Percent presence of the 41 common species in each cluster
- Clusters ordered by sample size; saved as `cluster_species_presence.jpg`

**Spatial distribution**
- UTM scatterplots of sampling locations colored by cluster, faceted by pool
- Before/after breakpoint spatial maps with jitter: `assemblage_location_break.jpg`

**Temporal dynamics — segmented regression**
For each pool × cluster combination, fits a continuous piecewise linear (segmented) regression to annual cluster proportions:
- Breakpoint location (year) estimated via `scipy.optimize.curve_fit`
- Breakpoint constrained to the interior 85% of the observed year range
- Compared to simple linear model via F-test (note: p-values are anti-conservative due to the Davies problem; treated as screening heuristics)
- Requires ≥ 6 annual observations and ≥ 4 nonzero proportions

Significant breakpoints (p < 0.05) identified in: Lower Pool 4 Cluster 4, Pool 8 Clusters 1 & 3, Pool 13 Clusters 1, 2, & 4

**Figures saved:**
| File | Description |
|------|-------------|
| `cluster_species_presence.jpg` | Species × cluster presence heatmap |
| `segmented_regression_clusters.jpg` | Time series with segmented regression fits by pool |
| `stacked_cluster_proportion_by_year_pool.jpg` | Stacked bar chart of annual cluster proportions |
| `cluster_pool_proportion.jpg` | Cluster proportions by pool (all years) |
| `cluster_aqua_desc_proportion.jpg` | Cluster proportions by aquatic habitat type |
| `cluster_pool_proportion_comparison.jpg` | Mean annual proportions before vs. after breakpoint by pool |
| `cluster_aqua_desc_proportion_comparison.jpg` | Mean annual proportions before vs. after breakpoint by habitat type |
| `assemblage_location_break.jpg` | Spatial maps before and after breakpoint |
| `cluster_avg_proportion_pool_slopegraph.jpg` | Slope graphs of before/after proportions by pool |
| `cluster_aqua_slopegraph.jpg` | Slope graphs of before/after proportions by habitat type |

---

## Dependencies

```
pandas
numpy
scipy
matplotlib
seaborn
scikit-learn
plotnine
tol_colors
tqdm
```

Install with:
```bash
pip install pandas numpy scipy matplotlib seaborn scikit-learn plotnine tol-colors tqdm
```
or
```bash
pip install -r requirements.txt
```
---

## Workflow

Run notebooks in order:

```
1data_wrangling.ipynb  →  pandas/*.csv  →  2cluster_analysis.ipynb  →  pandas/*_cluster1.csv  →  3cluster_visualization.ipynb  →  figures (*.jpg)
```

Intermediate files are cached in the `pandas/` directory between notebooks.
