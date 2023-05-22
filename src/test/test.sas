/* Set the location of your CSV file */
filename mydata '/path/to/your/file.csv';

/* Import the data from the CSV file */
proc import datafile=mydata out=mydata dbms=csv replace;
run;

/* Calculate the mean and standard deviation of a variable in the dataset */
proc means data=mydata;
var myvariable;
run;