
bs_mu  <- function(x) {
  data_b  <- sample_n(casen2017_mujeres, 
  size=nrow(casen2017_mujeres), 
  replace=TRUE)
  mu_muestra_b    <- mean(data_b$ingreso, na.rm=T)
  return(mu_muestra_b)
}

set.seed(77623)
distmuestral_boot <- replicate(5000, bs_mu()) %>% as_tibble()
glimpse(distmuestral_boot)

