# Import the requests to access websites, bs4 (Beautiful Soup) to parse XML
import requests
import bs4
import os

zipfile_link_path = './zipfile_links.txt'

if not (os.path.isfile(zipfile_link_path)):
	f_beg = open(zipfile_link_path,"w")
	f_beg.close()
	print ('zipfile_links.txt created')

bulkdata_scraper = requests.get('https://bulkdata.uspto.gov')
print ('Accessed USPTO bulkdata site')

# XML Parsing of main bulkdata website
bs_obj_main = bs4.BeautifulSoup(bulkdata_scraper.text, 'lxml')

# This variable gets information untill this year
till_date = 2001;

f_link_reader = open("zipfile_links.txt", 'r')
list_of_zipfile_links = f_link_reader.readlines()

# Loop over all the required links in the Bulkdata website (http://bulkdata.uspto.gov)
print ('Checking and writing if links are not present in the file. This may take few seconds...\n')
for a in bs_obj_main.find_all('a', href = True):

	if ('application' in a['href'] and 'fulltext' in a['href'] and int(a['href'].split('/')[-1]) >= till_date):

		#Accessing sub sites in USPTO bulk data storgae
		main_http = a['href']
		sub_scraper = requests.get(a['href'])

		# Parse sub sites
		bs_obj_sub = bs4.BeautifulSoup(sub_scraper.text, 'lxml')

		# Loop over all the tags and filter out the required '.zip' files for each sub sites
		for a in bs_obj_sub.find_all('a', href = True):
			if(('ipa' in a['href'] and '.zip' in a['href']) or ('pa' in a['href'] and '.zip' in a['href'])):
				zip_links = main_http + '/' + a['href'] + '\n'

				#Check if the link is present in the zipfile_links.txt
				if(zip_links not in list_of_zipfile_links):
					print (zip_links + 'is not in zipfile_links.txt')
					print ('Appending...')
					# Append links to zipfile_links.txt
					with open('zipfile_links.txt', 'a') as f_link_writer:
						f_link_writer.write(zip_links)
					print ('Done\n')

f_link_reader.close()
print ('zipfile_links.txt updated')
