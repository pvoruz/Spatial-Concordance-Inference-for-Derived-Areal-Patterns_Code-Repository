# Manuscript-safe semi-synthetic health application

The methodological case study uses a strict semi-synthetic design. Geographic support and
population denominators are specified from the official Geneva SITG population-by-statistical-
subsector layer (OCS_POPULATION_SSECTEUR; EPSG:2056), whereas all clinical geography is
synthetic.

The synthetic sample is calibrated only to publicly reported aggregate characteristics of a
Geneva hospitalized traumatic brain injury cohort: 1,071 hospitalized cases overall, including
678 adults aged 60 years or older and 393 adults aged 18–59 years. These counts constrain only
the numbers of simulated events. No observed patient address, empirical hotspot polygon,
cluster centroid, patient-level clinical trajectory, or unpublished spatial feature is used.

Within age stratum g:
(C_1g,...,C_mg) ~ Multinomial(N_g, pi_1g,...,pi_mg)
with
pi_ig = P_ig exp(beta R_ig) / sum_j P_jg exp(beta R_jg),
where P_ig is the official age-specific denominator and R_ig is a de novo seeded synthetic
spatial-risk field generated independently of the empirical TBI map.

The primary pattern operator classifies the 10% of units with the highest estimated log-relative
risk. RR>1.5 is a secondary variable-mass operator and is not tuned if non-estimable.

This is a methodological demonstration and must not be interpreted as an empirical replication,
validation, or new localization result for TBI in Geneva.
