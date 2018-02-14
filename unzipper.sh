# Make 'raw_data' directory if non existent
if [ ! -d "./raw_data" ]
then 
	mkdir raw_data
fi 

# Change directory to 'raw_data'
cd ./raw_data

# Make a 'downloaded.log' file if non existent
if [ ! -f "./downloaded.log" ]
then
	touch downloaded.log
fi

cp -v ../zipfile_links.txt ./

# Loop over all the downloadable links in the 'zipfile_links.txt' file 
for line in $(less zipfile_links.txt); 
do 
	# Get zip file name
	zip_file=$(echo ${line} | cut -d '/' -f 10)

	# Get name in XML extension
	# in_xml=$(echo ${zip_file} |  sed 's/\([a-z0-9]*\).*/\1/' | awk '{print $1".xml"}')
	
	# Check if the .xml file is present, if absent download the file (wget), and unzip and delete the zip file
	if [ -z $(grep "$zip_file" downloaded.log) ]
	then
		wget --continue  ${line}
		if [ $? -eq 0 ]
		then
			unzip ${zip_file}
			rm ${zip_file}
			echo ${zip_file} >> downloaded.log
		fi
	fi
done
