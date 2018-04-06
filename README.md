# edgar-analytics-insightdatachallenge
Used Python to solve this challenge. Here is the summary of my approach to the challenge:
1. Read the records from the input log.csv by retrieved the corresponding fields based on their header names.
2. Implemented a data dictionary with ip as a key and an object with attributes as reuest time, last request time, count of web page requests and inactivity count. In this way each ip has an instance of its own and corresponding variables.
3. For each record in the input stream, the combination of date and time(Timestamp) is verified to see if it has changed from the previous record/request. If it isn't, the dictionary is eithed added or updated with the record data based on whether if it is already existing in it or not.
4. The inactivity instance variable of each ip is used to check if for the time of current request, any ip session is active or expired. If it is expired, it is removed from the dictionary.
5. When a session is expired, the session details are logged onto the output file.
6. At the end of the file, all the sessions are closed and logged in the order of theri insertion into the dictionary. Ordered Dictionary is used for this purpose.
