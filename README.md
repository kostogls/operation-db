# operation-db
operationalization of ai4netmon project

The main script that runs the entire code is "main.py", that can be executed with: 

  ```
docker-compose up
  ```
ran in the terminal of the repo directory. 

## Repo description

This code downloads, processes and saves all the network datasets that we use in our ai4netmon project.

First, it downloads the misc datasets from various online sources, and aggregates them all together in a csv file, the aggregated_dataframe.csv. Then it calculates bias, distribution files and 
bias causes (differnces in distributions) per platform (RIPE Atlas, RIPE RIS, RouteViews etc.) and for Route Collectors (rrc). Finally, after all the neccessary files are produced and saved in the 
local code directory, all the files are saved in our MongoDB, in their corresponing collection. 
The datasets and  aggregated dataframe are saved using the date of the day that the script is executed. Everytime the scripts are executed again, except the whole process that was described above, the code compares
the previous date's datasets with the current downloaded datasets, and saves their differences in df_changes.csv. When the whole code has been executed, the previous date's files are removed, all the extracted files from the processes
that run inside the scrips are updated with the new calculated data and only the current date's misc data are saved in the local directory, as well as in the database. 

This whole process is supposed to run every month. 
