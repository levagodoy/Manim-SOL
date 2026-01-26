
bs_median  <- function(x) {
  data_b  <- sample_n(casen2017_mujeres, 
  size=nrow(casen2017_mujeres), 
  replace=TRUE)
  median_muestra_b <- median(data_b$ingreso, na.rm=T)
  return(median_muestra_b)
}

set.seed(77623)
distmuestral_boot <- replicate(5000, bs_median()) %>% as_tibble()
glimpse(distmuestral_boot)