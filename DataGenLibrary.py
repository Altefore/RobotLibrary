#DataGenLibrary for Robot 
#Author: Jonathan Light
#Date:	7/26/2016
#This python script contains a library of keywords that can be used to generate random data
#Most of the keywords call methods from the Faker library to generate the data


import random
import time 
import datetime 
import csv
import os
import timeit

from faker import Faker

global_windows_base_path = "C:\\Projects-GIT\\"
global_linux_base_path = "/srv/Jenkins/jobs/"
global_slave_base_path = "C:\\Jenkins\\workspace\\"

# KEYWORDS:

__all__ = ['data__gen_real_addresses',
	'data_gen_full_names',
	'data_gen_first_names',
	'data_gen_last_names',
	'data_gen_fake_streets',
	'data_gen_fake_cities',
	'data_gen_states',
	'data_gen_fake_zipcodes',
	'data_gen_usernames',
	'data_gen_passwords',
	'data_gen_phone_numbers',
	'data_gen_emails',
	'data_gen_ssn',
	'data_gen_dob',
	'data_gen_new_accounts',
	'data_gen_full_identity',
	'data_gen_fake_addresses',
	'data_gen_gender',
	'data_gen_countries']

__version__ = '1.0' #current version of this library

'''
Library function:
creates a specified amount of fake data_object_list as data_objects
data_objects contain fields that a real applicant would need to apply for a test or new profile
'''

class DataGenLibrary:
	
	fake = Faker() # create a new faker object
	master_attribute_list = [] # list of lists. each list is a set of data that was requested by the user
	master_type_list = [] # list of attribute names ordered by first added to last added
	master_object_list = [] #list of data objects
	master_attribute_list_zipped = [] #master list of the zipped master_attribute_list
	
	def _workspace_path(self, relative_path_to_workspace):
		'''
	    Author: Chris Weiske\n
	    Created: 3/6/2014\n

	    Description: This module takes in arguments and returns a string of the workspace path.\n

		_*Args*_:\n
			relative_path_to_workspace - The location of the file including the project name : ie SWS/Datasheets/SWS_HappyPath_AccountCreation.csv\n

	    '''
		if "/" in os.getcwd():
			jenkins_workspace = global_linux_base_path + "/workspace/"
			return (jenkins_workspace + relative_path_to_workspace)
		elif "\\" in os.getcwd():
			windows_workspace = global_windows_base_path + relative_path_to_workspace.replace("/", "\\")
		if os.path.exists(windows_workspace):
			return (windows_workspace)
		else:
			slave_path = global_slave_base_path + "\\" + relative_path_to_workspace.replace("/","\\")
			return (slave_path)

	def _gen_real_address(self, max_line, file_name = 'MDM_US_Address.csv', file_location = 'GITProjects\\MDM\\Datasheets\\'):
		'''
		This method will parse a csv file and return the list of items within a random row
		'''
		file_path = self._workspace_path(file_location + file_name)
		
		with open(file_path, 'r') as csvfile:
		
			file_reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
			
			for line in xrange(0, random.randint(1, max_line)):
			
				element = str(file_reader.next())
				
			element = element.replace('[','')
			element = element.replace(']','')
			element = element.replace(',','')
			element = element.replace("'",'')
		
			return element

	def _file_max_row(self, file_name, file_location):
		'''
		Parses given file at given location to find the maximum row 
		'''
		file_path = self._workspace_path(file_location + file_name)
		
		with open(file_path, 'r') as csvfile:
		
			file_reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
			count = 0 
			
			for line in csvfile:
	
				count += 1

		return count
	
	def write_to_json(self, file_name = 'TimeStamp', file_location = 'C:\\Temp'):
		'''
		Write all generated data to a JSON file.\n
		
		All you need to type is the keyword, and all data that has been generated up\n
		to that point will be written in a JSON file as objects. Data will be grouped so that there will be one of each\n
		Type generated in each object.\n
		
		_*Args*_:\n 
			``file_name`` (string):	What you would like to name the file. Otherwise it will\n
			name the file as a timestamp at time of generation.\n
			``file_location`` (string): Default is Temp folder in C drive. Otherwise specify a \n
			location you would like the JSON file to be written to. Make sure to use \\ between foldes\n
		'''
		if file_name == 'TimeStamp':
		
			structTime = time.localtime()
			file_name = (str(datetime.datetime(*structTime[:6])).replace(' ','@')).replace(':','_',3)
		
		if not self.master_attribute_list:
		
			print('ERROR: No data has been generated. JSON file will not be written')
			return 
			
		if len(file_name) <= 5 or (len(file_name) >= 6 and file_name[len(file_name) - 5:len(file_name)] != '.json'):
			file_name = str(file_name) + '.json'
			
			self._zip_data()
			
			json_string = '{"data":['
			
			for list in self.master_attribute_list_zipped:
				json_string = json_string + '{'
				
				for i in xrange(0 ,len(list)):
					json_string = json_string + '"' + self.master_type_list[i] +  '":"' + list[i] + '", '
					
				json_string = json_string[:len(json_string) - 2] + '},'
				
			json_string = json_string[:len(json_string) - 1] + ']}'
			
			text_file = open(os.path.join(file_location,file_name), 'w')
			text_file.write(json_string)
		
		print('File: %s created successfully in dir %s' % (file_name, file_location))

	def write_to_csv(self,file_name = 'TimeStamp',file_location = 'C:\\Temp'):
		'''
		Write all generated data to a CSV file
		
		All you need to type is the keyword, and all data that has been generated up\n
		to that point will be written in a CSV file as objects. Data will be grouped so that there will be one of each\n
		type generated in each object.\n
		
		_*Args*_:\n 
			``file_name`` (string):	What you would like to name the file. Otherwise it will\n
			name the file as a timestamp at time of generation.\n
			``file_location`` (string): Default is Temp folder in C drive. Otherwise specify a \n
			location you would like the CSV file to be written to. Make sure to use \\ between foldes\n
		'''
		if file_name == 'TimeStamp':
			structTime = time.localtime()
			file_name = (str(datetime.datetime(*structTime[:6])).replace(' ','@')).replace(':','_',3)
		
		if not self.master_attribute_list:
			print('ERROR: No data has been generated. CSV file will not be written')
			return
			
		if len(file_name) <= 4 or (len(file_name) >= 5 and file_name[len(file_name) - 4:len(file_name)] != '.csv'):
			file_name = str(file_name) + '.csv'
		
		with open(os.path.join(file_location,file_name), 'wb') as csvfile:
			file_writer = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
			file_writer.writerow(self.master_type_list)	
			self._zip_data()
			for list in self.master_attribute_list_zipped:
				file_writer.writerow(list)
		
		print('File: %s created successfully in dir %s' % (file_name, file_location))
		
	def _zip_data(self):
		'''
		Treats data lists as a full matrix, then transposes it to be written in a file. 
		Used to group data to make it more readable
		
		Ex. zip{[2 , 2 , 2], [3 , 3 , 3]} = {[2, 3], [2, 3], [2, 3]}
		'''
		
		self.master_attribute_list_zipped = zip(*self.master_attribute_list)	
			
	def clear_all_data(self):
		'''
		Clears all data objects.

		All data generated before a call to this method will be deleted.
		'''
		
		self.master_attribute_list = []
		self.master_type_list = []
		self.master_object_list = []
		self.master_attribute_list_zipped = []
		
		print("SUCCESS: All data has been erased.")
	
	def _check_object_list(self,count = 1000):
		'''
		Checks for empty or underpopulated list and populates it according to the count
		'''
		
		if not self.master_object_list:
		
			for object in xrange(0,count):
				self.master_object_list.append(fake_data_object())
		
		elif len(self.master_object_list) < count:
		
			for object in xrange(len(self.master_object_list), count):
				self.master_object_list.append(fake_data_object())
				
	def _check_file_path(self, path):
		'''
		Checks for a valid directory 
		'''
		return os.path.exists(path)
	
	
	# KEYWORDS:
	
		
	def data__gen_real_addresses(self, count = 100, file_name = 'MDM_US_Address.csv', file_location = 'GITProjects\\MDM\\Datasheets\\'):
		'''
		Pulls a valid address from a datasheet and stores it in a list\n 
		
		This address is stored in a list to either be written to a file or returned as an argument\n
		
		_*Args*_:\n 
			``count`` (int):	The number of addresses you would like to generate\n
			
		_*Returns*_:\n		
			``real_address_list`` (list): List of addresses 
		'''
		
		count = int(count)
		max_line = self._file_max_row(file_name, file_location)
		real_address_list = [] 
		for object in xrange(0,count):
			real_address_list.append(self._gen_real_address(max_line, file_name, file_location))
		self.master_attribute_list.append(real_address_list) #Would be better to parse first line of sheet for names
		self.master_type_list.append('Address')
		
		
		return real_address_list
	
	def data_gen_full_names(self, count = 1000, middle_initial = 'N'):
		'''
		This method will generate full names\n
		
		Once generated, these names can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``middle_initial`` (string or char): 'Y' if you would like to include the middle inital, anything else otherwise\n
		
		_*Returns*_:\n
			``full_name_list`` (list): a list of generated names as strings\n
		
		_*Example*_:\n
			>>> data_gen_full_names(2, 'N')\n
			[Peter Parker, Scott Graves]\n
		'''
		
		count = int(count)
		self._check_object_list(count)
		full_name_list = []
		
		for object in xrange(0,count):
			full_name_list.append(str(self.master_object_list[object].gen_name_full(middle_initial)))
			
		self.master_attribute_list.append(full_name_list)
		self.master_type_list.append('Full_Names')
		
		return full_name_list
	
	def data_gen_first_names(self, count = 1000):
		'''
		This method will generate first names\n
		
		Once generated, these names can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
		
		_*Returns*_:\n
			``first_name_list`` (list): a list of generated names as strings\n
		
		_*Example*_:\n
			>>> data_gen_first_names(2)\n
			[John, Hilda]\n
		'''
		
		count = int(count)
		self._check_object_list(count)
		first_name_list = []
		
		for object in xrange(0,count):
			first_name_list.append(str(self.master_object_list[object].gen_name_first()))
			
		self.master_attribute_list.append(first_name_list)
		self.master_type_list.append('First_Names')
		
		return first_name_list
	
	def data_gen_last_names(self, count = 1000):
		'''
		This method will generate last names\n
		
		Once generated, these names can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
		
		_*Returns*_:\n
			``last_name_list`` (list): a list of generated names as strings\n
		
		_*Example*_:\n
			>>> data_gen_last_names(2)\n
			[Zieme, Simonis]\n
		'''
		
		count = int(count)
		self._check_object_list(count)
		last_name_list = []
		
		for object in xrange(0,count):
			last_name_list.append(str(self.master_object_list[object].gen_name_last())) 
			
		self.master_attribute_list.append(last_name_list)
		self.master_type_list.append('Last_Names')
		
		return last_name_list
	
	def data_gen_fake_zipcodes(self, count = 1000, plus4 = 'N'):
		'''
		This method will generate fake zipcodes\n
		
		Once generated, these zipcodes can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``plus4`` (string): 'Y' for included, 'N' for excluded\n
		_*Returns*_:\n
			``zipcode_list`` (list): a list of generated zipcodes as strings\n
		
		_*Example*_:\n
			>>> data_gen_fake_zipcodes(2)\n
			[23447, 61440]\n
		'''
		count = int(count)
		self._check_object_list(count)
		zipcode_list = []
		
		for object in xrange(0,count):
			zipcode_list.append(str(self.master_object_list[object].gen_fake_address_zip(plus4))) 
			
		self.master_attribute_list.append(zipcode_list)
		self.master_type_list.append('Zipcodes')
		
		return zipcode_list
		
	def data_gen_fake_streets(self, count = 1000, ):
		'''
		This method will generate fake street addresses\n
		
		Once generated, these streets can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			
		_*Returns*_:\n
			``street_list`` (list): a list of generated streets as strings\n
		
		_*Example*_:\n
			>>> data_gen_fake_streets(2)\n
			[770 Albertha Corner, 3850 Harris Fall]\n
		'''
		
		count = int(count)
		self._check_object_list(count)
		street_list = []
		
		for object in xrange(0,count):
			street_list.append(str(self.master_object_list[object].gen_fake_address_street())) 
			
		self.master_attribute_list.append(street_list)
		self.master_type_list.append('Streets')
		
		return street_list
	
	def data_gen_fake_cities(self, count = 1000):
		'''
		This method will generate fake cities\n
		
		Once generated, these cities can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			
		_*Returns*_:\n
			``city_list`` (list): a list of generated cities as strings\n
		
		_*Example*_:\n
			>>> data_gen_fake_cities(2)\n
			[Lake Urbanland, Kuvalisburgh]\n
		'''
		count = int(count)
		self._check_object_list(count)
		city_list = []
		
		for object in xrange(0,count):
			city_list.append(str(self.master_object_list[object].gen_fake_address_city())) 
			
		self.master_attribute_list.append(city_list)
		self.master_type_list.append('Cities')
		
		return city_list
		
	def data_gen_states(self, count = 1000, abrev = 'Y'):
		'''
		This method will generate states\n
		
		Once generated, these states can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``abrev`` (sring): 'Y' for abreviation, else for otherwise\n
			
		_*Returns*_:\n
			``state_list`` (list): a list of generated stataes as strings\n
		
		_*Example*_:\n
			>>> data_gen_states(2)\n
			[Nevada, Vermont]\n
		'''
		
		count = int(count)
		self._check_object_list(count)
		state_list = []
		
		for object in xrange(0,count):
			state_list.append(str(self.master_object_list[object].gen_fake_address_state(abrev)))
			
		self.master_attribute_list.append(state_list)
		self.master_type_list.append('States')
		
		return state_list
	
	def data_gen_usernames(self, count = 1000, name_dependant = 'Y'):
		'''
		This method will generate user names\n
		
		Once generated, these user names can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``name_dependant``(string): 'Y' for the username to depend on a previously generated name, else for otherwise\n
			
		_*Returns*_:\n
			``username_list`` (list): a list of generated user names as strings\n
		
		_*Example*_:\n
			>>> data_gen_usernames(2, 'Y')\n
			[yasmeenxzieme, marjory-simonis]\n
		'''		
		
		count = int(count)
		self._check_object_list(count)
		username_list = []
		
		for object in xrange(0,count):
			username_list.append(str(self.master_object_list[object].gen_user_name(name_dependant)))
			
		self.master_attribute_list.append(username_list)
		self.master_type_list.append('User_Names')
		
		return username_list
		
	def data_gen_passwords(self, count = 1000, min = '6', max = '16', contain_special = 'Y', contain_number = 'Y', contain_upper = 'Y', contain_lower = 'Y'):
		'''
		This method will generate random passwords\n
		
		Once generated, these passwords can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``min`` (int): minimum number of characters you would like your password to be\n
			``max`` (int): maximum number of characters you would like your password to be\n
			``contain_special`` (string): 'Y' for passwords with special characters, else for otherwise\n
			``contain_number`` (string): 'Y' for passwords with numbers, else for otherwise\n
			``contain_upper`` (string): 'Y' for passwords with uppercase characters, else for otherwise\n
			``contain_lower`` (string): 'Y' for passwords with lowercase characters, else for otherwise\n
			
		_*Returns*_:\n
			``password_list`` (list): a list of generated passwords as strings\n
		
		_*Example*_:\n
			>>> data_gen_passwords(2, 10, 14, 'y', 'N', 'Y', '')\n
			[CTYNSBI&G*(Z$#, IFZ+*S#JNX@G]\n
		'''	
		count = int(count)
		self._check_object_list(count)
		password_list = []
		
		for object in xrange(0,count):
			password_list.append(str(self.master_object_list[object].gen_password(min, max, contain_special, contain_number, contain_upper, contain_lower)))
			
		self.master_attribute_list.append(password_list)
		self.master_type_list.append('Passwords')
		
		return password_list
	
	def data_gen_phone_numbers(self, count = 1000, format = '1(xxx)xxx-xxxx'):
		'''
		This method will generate phone numbers\n
		
		Once generated, these phone numbers can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``format``(string): the method will fill in a phone number when given a format containing Xs\n
			
		_*Returns*_:\n
			``phone_number_list`` (list): a list of generated phone numbers as strings\n
		
		_*Examples*_:\n
			>>> data_gen_phone_numbers(2, '1(xxx)xxx-xxxx')\n
			[1(907)764-3886, 1(165)888-0762]\n
			
			>>> data_gen_phone_numbers(2, '312_xxx_XXX9')\n
			[312_631_8499, 312_452_3229]
		'''	
		count = int(count)
		self._check_object_list(count)
		phone_number_list = []
		
		for object in xrange(0,count):
			phone_number_list.append(str(self.master_object_list[object].gen_phone_number(format))) 
			
		self.master_attribute_list.append(phone_number_list)
		self.master_type_list.append('Phone_Numbers')
		
		return phone_number_list
	
	def data_gen_emails(self, count = 1000, domain = 'random', name_dependant = 'Y', contains_numbers = 'Y'):
		'''
		This method will generate fake emails\n
		
		Once generated, these emails can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``domain`` (string): if you would like emails to have a specific domain, enter it  here as '@domain.blah' , otherwise enter 'random'\n
			``name_dependant`` (string): any names have been generated, the emails generated will\n
			depend on those names. 'Y' for name dependant, else for otherwise\n
			``contains_numbers`` (string): 'Y' for a chance that the email contains numbers, else for otherwise\n
		_*Returns*_:\n
			``email_list`` (list): a list of generated emails as strings\n
		
		_*Example*_:\n
			>>> data_gen_emails(2)\n
			[cindaxbernhard@nicolas-bayer.com, NathaliaMarvin51@yahoo.com]\n
		'''	
		count = int(count)
		self._check_object_list(count)
		email_list = []
		
		for object in xrange(0,count):
			email_list.append(str(self.master_object_list[object].gen_email(domain, name_dependant, contains_numbers)))
			
		self.master_attribute_list.append(email_list)
		self.master_type_list.append('Emails')
		
		return email_list
		
	def data_gen_ssn(self, count = 1000):
		'''
		This method will generate fake Social Security Numbers\n
		
		Once generated, these SSNs can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
		
		_*Returns*_:\n
			``ssn_list`` (list): a list of generated SSNs as strings\n
		
		_*Example*_:\n
			>>> data_gen_ssn(2)\n
			[121-80-7422, 020-12-1295]\n
		'''	
		
		count = int(count)
		self._check_object_list(count)
		ssn_list = []
		
		for object in xrange(0,count):
			ssn_list.append(str(self.master_object_list[object].gen_ssn()))
			
		self.master_attribute_list.append(ssn_list)
		self.master_type_list.append('SSNs')
		
		return ssn_list
		
	def data_gen_dob(self, count = 1000, format = 'mm/dd/yyyy', min = '1970', max = 'now'):
		'''
		This method will generate dates\n
		
		Once generated, these dates can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``format`` (string): mm will be replaced by month, dd will be replaced by day, and yy or yyyy will be replaced by the year\n
			Any kind of format will be filled in by the generator (Look at example for clarification)
			
		_*Returns*_:\n
			``dob_list`` (list): a list of generated DOBs as strings\n
		
		_*Example*_:\n
			>>> data_gen_dob(2, 'mm/dd/yy', '1975', '1999')\n
			[01/20/85, 07/20/76]\n
			>>> data_gen_dob(2, 'mm:dd:yyyy')\n
			[07:01:1988, 02:09:1999]\n
		'''	
		count = int(count)
		self._check_object_list(count)
		dob_list = []
		
		for object in xrange(0,count):
			dob_list.append(str(self.master_object_list[object].gen_dob(min, max, format)))
			
		self.master_attribute_list.append(dob_list)
		self.master_type_list.append('Date_of_Birth')
		
		return dob_list
		
	def data_gen_gender(self, count = 1000, gender = ''):
		'''
		This method will generate genders\n
		
		Once generated, these genders can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			``gender`` (string): 'M' for all male, 'F' for all female\n

		_*Returns*_:\n
			``gender_list`` (list): a list of generated genders as strings\n
		
		_*Example*_:\n
			>>> data_gen_gender(2)\n
			[F, M]\n
			>>> data_gen_gender(2, 'F')\n
			[F, F]\n
		'''			
		
		count = int(count)
		self._check_object_list(count)
		gender_list = []
		
		for object in xrange(0,count):
			gender_list.append(str(self.master_object_list[object].gen_gender(gender)))
			
		self.master_attribute_list.append(gender_list)
		self.master_type_list.append('Gender')
		
		return gender_list
	
	def data_gen_countries(self, count = 1000):
		'''
		This method will generate countries\n
		
		Once generated, these countries can be written to a csv file by calling ``write_to_csv`` or a json file by calling ``write_to_json``\n\n
		
		_*Args*_:\n
			``count`` (int): amount you would like to generate\n
			
		_*Returns*_:\n
			``country_list`` (list): a list of generated countries as strings\n
		
		_*Example*_:\n
			>>> data_gen_countries(2)\n
			[Morocco, Iceland]\n
		'''	
		
		count = int(count)
		self._check_object_list(count)
		country_list = []
		
		for object in xrange(0,count):
			country_list.append(str(self.master_object_list[object].gen_country()))
			
		self.master_attribute_list.append(country_list)
		self.master_type_list.append('Country')
		
		return country_list
		
	def data_gen_new_accounts(self, count = 1000):
		'''
		This method will generate new account information
		
		This is a combination of full names, usernames, emails and passwords
		
		_*Args*_:\n
			``count`` (int):	The number of accounts you would like to generate
		
		_*Returns*_:\n
			``accounts`` (list of lists): Each list within the list is a seperate account 
		'''
		
		count = int(count)
		account = self.data_gen_full_names(count)
		account.append(self.data_gen_usernames(count))
		account.append(self.data_gen_emails(count))
		account.append(self.data_gen_passwords(count))
		
		return account
		
	def data_gen_fake_addresses(self, count = 1000):
		'''
		Generates fake full addresses and returns them in a list\n 
		
		This list can then be written to a file or returned as an argument\n
		
		_*Args*_:\n 
			``count`` (int):	The number of addresses you would like to generate\n
			
		_*Returns*_:\n		
			``full_address_list`` (list): List of fake addresses 
		'''
		
		count = int(count)
		self._check_object_list(count)
		full_address_list = []
		
		for object in xrange(0,count):
			full_address_list.append(str(self.master_object_list[object].gen_address_full()))
			
		self.master_attribute_list.append(full_address_list)
		self.master_type_list.append('Fake_Address')
		
		return full_address_list
					
	def data_gen_full_identity(self, count = 1000):
		'''
		Uses pre-esisting keywords to create a fake identity
		
		Generates full names, Dates of Birth, real addresses, phone numbers, emails, usernames, passwords, and social security numbers 
		
		_*Args*_:\n
			``count`` (int): How many identities you would like to generate 
		
		_*Returns*_:\n
			``identity`` (list of lists): each list is a type of data (email, usernames)
		'''
		
		count = int(count)
		identity = self.data_gen_full_names(count)
		identity.append(self.data_gen_gender(count))
		identity.append(self.data_gen_dob(count))
		identity.append(self.data__gen_real_addresses(count))
		identity.append(self.data_gen_phone_numbers(count))
		identity.append(self.data_gen_emails(count))
		identity.append(self.data_gen_usernames(count))
		identity.append(self.data_gen_passwords(count))
		identity.append(self.data_gen_ssn(count))
		
		return identity
		
				
	
# class fake_data_object, once initialized, contains random fake information that acts as an identity for a completely fictitious data_object
class fake_data_object:

	
	_address_city = '--'
	_address_full = '--'
	_address_state = '--'
	_address_street = '--'
	_address_zip = '--'
	_dob = '--'
	_email = '--'
	_ethnicity = '--'
	_gender = '--'
	_middle_init = '--'
	_name_first = '--'
	_name_full = '--'
	_name_last = '--'
	_name_middle = '--'
	_password = '--'
	_phone_number = '--'
	_ssn = '--'
	_user_name = '--'
	_country = '--'
	
	fake = Faker()
	
	'''
	Data Generator Methods
	These methods, when called, generate random data within the object 
	'''

	def gen_name_first(self, parameters = ''):
		self._name_first = self.fake.first_name()
		return self._name_first
		

	def gen_name_last(self, parameters = ''):
		self._name_last = self.fake.last_name()
		return self._name_last
		

	def gen_name_middle(self, parameters = ''):
		self._name_middle = (self.fake.first_name() or self.fake.last_name())
		self.gen_middle_init()
		return self._name_middle
		
	
	def gen_middle_init(self, parameters = ''):
		self._middle_init = self._name_middle[0]
		

	def gen_name_full(self, middle_initial = 'Y'):
		
		if self._name_first == '--':
			self.gen_name_first()
			
		if self._name_middle == '--' and middle_initial.upper() == 'Y':
			self.gen_name_middle()
			
		if self._name_last == '--':
			self.gen_name_last()
		
		self._name_full = self._name_first 
		
		if middle_initial.upper() == 'Y':
			self._name_full += (" " + self._name_middle[0] + ".")
			
		self._name_full += (" " + self._name_last)
		
		return self._name_full
			
	def gen_dob(self, min = '1970', max = 'now', format = 'mm-dd-yyyy' ):
		
		if min == '1970' and (max == '' or max.lower() == 'now'):
			self._dob = self.fake.date_time()
		
		elif (not max.lower() == 'now') and (int(max) >= int(min) and (int(min) >= 1970 and int(max) > 1970) and (int(max) < 2050 and int(min) < 2049)):
			this_year = int(datetime.date.today().year)
			max = str(int(max) - this_year) + 'y'
			min = str(int(min) - this_year) + 'y' 
			self._dob = self.fake.date_time_between(start_date = min, end_date = max)

		year = self._dob.year
		month = self._dob.month
		day = self._dob.day
		return(self.format_date(str(day), str(month), str(year), format))
	

	def format_date(self, day, month, year, format):
		count = len(format) - 1 
		y_count = len(year) - 1
		m_count = len(month) - 1
		d_count = len(day) - 1
		
		if m_count == 0: 
			month = '0' + month
			m_count = 1
			
		if d_count == 0:
			day = '0' + day
			d_count = 1
			
		for i in xrange(0,len(format)):
		
			if format[count].lower() == 'y' and y_count >= 0:
				format = format[:count] + format[count:].replace('y',year[y_count])
				y_count-=1
				
			elif format[count].lower() == 'm' and m_count >= 0:
				format = format[:count] + format[count:].replace('m',month[m_count])
				m_count-=1
				
			elif format[count].lower() == 'd' and d_count >= 0:
				format = format[:count] + format[count:].replace('d',day[d_count])
				d_count-=1
				
			count -= 1
		return format
		
	
	def gen_fake_address_street(self, parameters = ''):
		self._address_street = self.fake.street_address()
		return self._address_street


	def gen_fake_address_city(self, parameters = ''):
		self._address_city = self.fake.city()
		return self._address_city
		

	def gen_fake_address_state(self, abrev = 'Y'):
	
		if abrev.lower() == 'y':
			self._address_state = self.fake.state_abbr()
		
		else:	
			self._address_state = self.fake.state()
		
		return self._address_state


	def gen_fake_address_zip(self, plus4 = 'N'):
		
		if plus4.lower() == 'y':
			self._address_zip = str(self.fake.zipcode_plus4())
		
		else:
			self._address_zip = str(self.fake.zipcode())
		
		return self._address_zip


	def gen_address_full(self, parameters = ''):
		
		if self._address_city == '--':
			self.gen_fake_address_city()
		
		if self._address_state == '--':
			self.gen_fake_address_state()
		
		if self._address_street == '--':
			self.gen_fake_address_street()
		
		if self._address_zip == '--':
			self.gen_fake_address_zip()
			
		self._address_full = self._address_street + "; " + self._address_city + " " + self._address_state + " " + self._address_zip
		
		return self._address_full
		
	
	def gen_email(self, domain = 'random', name_dependant = 'Y', contains_numbers = 'Y' ):
		
		if not self._email == '--':
			return self._email
		
		self._email = self.fake.email()
		domain = str(domain)
		
		if name_dependant.lower() == 'y':
			email_end = self._email[self._email.index('@'):len(self._email)]
			rand = random.randint(0,2)
			name = self.gen_name_full('n')
			
			# separated by deliminator [.,_,-,x]
			if rand == 0:
				name = name.replace(' ',random.choice("._-x")).lower()
			
			#first initial plus last name
			if rand == 1:
				name = name[0] + name[name.index(' '):len(name)]
				name = name.replace(' ','').lower()
			
			#first plus last name
			if rand == 2:
				name = name.replace(' ','')
			
			# if containts_numbers, 1 in 4 chance to have a number at the end_date 
			if random.randint(0,3) == 0 and contains_numbers.lower() == 'y':
				name += str(random.randint(0,1000))
				
			if domain == 'random':
				self._email = name + email_end
			
			elif '@' in domain:
				self._email = name + domain
			
			else:
				self._email = name + '@' + domain
	
		return self._email
			

	def gen_user_name(self, name_dependant = 'Y'):
		
		if name_dependant.lower() == 'y':
			self._user_name = self.gen_email()
			self._user_name = self._user_name[:self._user_name.index('@')]
		
		else:
			self._user_name = self.fake.user_name()
		
		return self._user_name
		
	def gen_password(self, min = '4', max = '16', contain_special = 'Y', contain_number = 'Y', contain_upper = 'Y', contain_lower = 'Y'):
		
		if int(min) < 4:
			min = '4'
		
		if int(max) < int(min):
			max = min
	
		if contain_special.lower() == 'y': special = True 
		else: special = False
		if contain_number.lower() == 'y': digits = True 
		else: digits = False
		if contain_upper.lower() == 'y': upper = True 
		else: upper = False
		if contain_lower.lower() == 'y': lower = True 
		else: lower = False
		
		length = random.randint(int(min),(int(max)))
		
		if(lower or special or digits or upper):
		
			self._password = self.fake.password(length, special, digits, upper, lower)
			
			while not self.password_check(length, special, digits, upper, lower):
				self._password = self.fake.password(length, special, digits, upper, lower)

			
		return self._password
	
	# Checks to make sure password has all requirements
	def password_check(self, length, special, digits, upper, lower):
		special = not special
		digits = not digits
		upper = not upper
		lower = not lower
		
		for c in xrange(0,len(self._password)):
			
			if self._password[c].islower():
				lower = True
				continue
			
			if self._password[c].isupper():
				upper = True
				continue
			
			if self._password[c].isnumeric():
				digits = True
				continue
			
			else:
				special = True
			
		return (special and digits and upper and lower)
		
		
	def gen_phone_number(self, format = '1(xxx)xxx-xxxx'):
		count = len(format) - 1
		
		for i in xrange(0,len(format)):
			
			if format[count].lower() == 'x':
				format = format[:count] + format[count:].replace('x',str(random.randint(0,9)))
				format = format[:count] + format[count:].replace('X',str(random.randint(0,9)))
			
			count -= 1
		
		self._phone_number = format			
		return self._phone_number


	def gen_gender(self, gender = ''):
		
		if gender.lower() == 'f':
			self._gender = 'F'
		
		elif gender.lower() == 'm':
			self._gender = 'M'
		
		else:
			
			if random.randint(0,1):
				self._gender = 'F'
			
			else:
				self._gender = 'M'
			
		return self._gender
	

	def gen_ssn(self, parameters = ''):
		self._ssn = self.fake.ssn()
		
		return self._ssn
	
	def gen_country(self, parameters = ''):
		self._country = self.fake.country()
		
		return self._country
	
