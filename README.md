# traffic-sim-braess
This is the repository for the project "Improving Almaty’s Transport Routes Based on Braess Paradox" by Yerzhan Yerkezhan and Danay Zhaniya

The aim of the works is to find Braess Links in Almaty's road network. As a result of the research, parts of the Kozhamkulov and Shchepetkov Streets and Utegen Batyr Street were defined as Braess Links and were removed in the modified network. You can see their image at .png files.

alma_config.xml is the configuration file that was used for both modified and original networks. It was developed based on official MATSim example projects. We made up for our small population sample by modifying the MATSim configuration's capacity parameters. This ensures that our 500 agents encounter the typical bottleneck of Almaty by simulating the limitations of a densely populated city.

almaty.py is the python file that was used to create the population files (population_500.xml) for both modified and original networks. It was created by dividing different regions. The areas were divided according to the likelihood that a job or home might be located there. Then, 3 types of groups of people were created (workers, students, and pensioners/housewives), and a daily plan was assigned for each of the groups.

in key results you can find key results for both networks.

in all_data.txt there is the link to Google Drive where you can find all of the folders that where used to create simulations, output folders and our research article.
How to get the output folder by yourself (if you want): install MATSim, insert the file alma_config.xml from the desired folder (almatyy is for original network and final is for modified network); press "Start MATSim" and you will get the output file.
How to run the viualization: install Via, insert network, event and plans files (extract from zip folders), load them and start the simulation.
