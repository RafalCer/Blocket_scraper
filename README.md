# Blocket_scraper

The program scrapes most recent ads on Blocket. The output is a csv file containing the following pieces of information about every ad: Ad name, Category, Price, Location, Time, Link, and ID. Note that since the information is in Swedish, the default csv reader might not recognize some of the characters. This can usually be fixed by changing the settings of the reader.

The default number of ads to be scraped is 40; however, it can be modified by adjusting the argument pages_to_scrape.  The program also accepts an optional argument for path where the csv file should be saved. If no path is specified, the file will be saved in the same directory as the python file.

The program can be run either through command prompt or through an IDE. In the first case, it can be run by changing the directory to the location of the file and running python blocket_scrapper.py. An example can be seen below:

>> python blocket_scraper.py --path "C:\\Users\\Rafa\\Desktop\\" --pages_to_scrape "3"
>> Corpus retrieved successfully

In the case of an IDE, one has to open blocket_scraper.py through an IDE such as Anaconda and simply run it. 
