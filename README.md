# SemanticMatch

Frequently Asked Questions (FAQ’s) semantic matching Application (NLP Application)     
        
Technology Used: Python, WordNet, Solr					      

Implemented a FAQ semantic matching application that would produce improved results using NLP features and techniques. Given a set of FAQ’s and Answers and a User’s input natural language question/statement, the application outputs top 10 FAQ’s and Answers that best match the user’s input question/statement.



Install Solr
o	Download solr-7.3.0.zip from the following link-
http://apache.osuosl.org/lucene/solr/7.3.0/


o	Extract the Zip folder in your machine. Now go to extracted solr folder. Get inside the example folder and execute the command
java -jar start.jar


o	As soon as you run the above command solr will start with default port 8983. That can be accessible on- 
http://localhost:8983/solr/#/


o	In command prompt go to the bin directory of the solr folder. 


o	Create solr core instance by: 
solr.cmd create -c collection_1


o	To run solr from bin director, give command
solr start

-	Install NLTK


o	pip install nltk
-	Install PySolr

o	pip install pysolr


First run Task4_Index in cmd
python Task4_Index.py 

Next run Task2
python Task2.py and enter the FAQ

To run Task3
python Task3.py

To run Task4_Match
python Task4_Match.py and enter the faq

