# AIDSDatabaseAnalysis
This is the database and Python code to analyze a subset of the CDC Wonder AIDS Database and automatically generate graphs.  
The database is in a sequence of *.sql files zipped into two zip files.  They should be extracted and imported into an SQL database program of choice.
Once compiled into a database, the python code must be modified to create a connection to the database for parsing.  The code currently uses pypyodbc for its Microsoft Access functionality.  Modification to use SQLAlchemy is relatively straight forward.  Once that is created, the code will automatically analyze the data and generate a number of graphs.
