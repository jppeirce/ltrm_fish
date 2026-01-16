# install.packages(c("dynamicTreeCut","vegan"))  # run once
library(dynamicTreeCut)
library(vegan)   # for Jaccard distances on binary data

fish_df <- read.csv("pandas/fish_df.csv", check.names = FALSE)
head(fish_df)

# Keep only species columns (0/1 presence). If needed, coerce strings to 0/1:
is_binary <- function(x) {all(x %in% c(0,1))}
fish_df <- fish_df[sapply(fish_df, is_binary)]   # adjust selection as appropriate
fish_df <- as.matrix(fish_df)                # samples (rows) × species (cols)


# Jaccard dissimilarities for presence/absence (ignores double zeros)
D <- vegdist(fish_df, method = "jaccard", binary = TRUE)    # dissimilarity (dist object)

hc <- hclust(D, method = "average")                  # HAC: average linkage + Jaccard
plot(hc, main = "HAC dendrogram (average + Jaccard)")
