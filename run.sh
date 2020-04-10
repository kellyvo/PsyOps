#!/bin/bash

# Checks to make sure that the input file exists
if [ ! -f input.txt ]; then
	echo "Input file input.txt does not exist. Store the inputs in this file."
	exit 1
fi

if [ $# -ne 1 ]; then
	echo "Wrong number of command line args. There should be 1 command line arg."
	exit 1

elif [ $1 != 'y' ] && [ $1 != 'n' ]; then
	echo "Wrong command line args. It should be [y/n] for whether or not this is a training set."
	exit 1
fi

if [ $1 == "y" ]; then

	# Changes all files into executables
	echo "Creating executables"
	
	chmod +x RedditScraper.py
	chmod +x training_data.py
	chmod +x fact_or_opinion.py
	chmod +x SVM.py

	# Installs the dependencies
	echo "Installing dependencies"
	
	pip install -U praw > /dev/null
	pip install -U bs4 > /dev/null
	pip install -U nltk > /dev/null
	pip install -U requests > /dev/null
	pip install -U scikit-learn > /dev/null
	python -m pip install -U matplotlib > /dev/null
	pip install -U numpy > /dev/null

	echo "Generating keywords. This may take a while."
	printf "Opinionated.txt\nUnopinionated.txt\n" | python3 training_data.py

	printf "" > training.txt

	# Trains the linear regression model
	echo "Getting data to train the support vector machine"

	# Reads the Opinionated text document
	while read input;
	do
	
		# Runs the script getting whether or not it is a fact or opinion
		OUTPUT="$(echo $input | python3 fact_or_opinion.py 2>/dev/null)"
		OUTPUT=${OUTPUT:5}

		# If the result is not an error (errors result if the article has
		# been deleted) add the output to the training file
	
		if [ ${#OUTPUT} -gt 10 ]; then
			echo "OPINIONATED ARTICLE" | tee -a training.txt
			echo $input | tee -a training.txt
			echo "${OUTPUT}" | tee -a training.txt
			printf "\n" | tee -a training.txt
		fi

	done < Opinionated.txt

	# Reads the unopinionated text document
	while read input;
	do
	
		# Runs the script getting whether or not it is a fact or opinion
		OUTPUT="$(echo $input | python3 fact_or_opinion.py 2>/dev/null)"
		OUTPUT=${OUTPUT:5}

		# If the result is not an error (errors result if the article has
		# been deleted) add the output to the training file
		if [ ${#OUTPUT} -gt 10 ]; then
			echo "NON-OPINIONATED ARTICLE" | tee -a training.txt
			echo $input | tee -a training.txt
			echo "${OUTPUT}" | tee -a training.txt
			printf "\n" | tee -a training.txt
		fi
	done < Unopinionated.txt
fi

echo "Scraping reddit for input"
python3 RedditScraper.py news

# Classifies the inputs
echo "Classifying the inputs. Again, this may take a while."

printf "" > output.txt

while read input;
do
	OUTPUT="$(echo $input | python3 fact_or_opinion.py 2>/dev/null)"
	OUTPUT=${OUTPUT:5}
	if [ ${#OUTPUT} -gt 10 ] ; then
		echo $input | tee -a output.txt
		echo "${OUTPUT}" | tee -a output.txt
		printf "\n" | tee -a output.txt
	fi
done < input.txt

if [ ! -f results.txt ]; then
    printf "" > results.txt
fi

python3 SVM.py | tee -a results.txt

#if [ $1 == "y" ]; then
#	python3 Linear_Regression.py yes | tee -a results.txt
#else
#	python3 Linear_Regression.py no | tee -a results.txt
#fi

echo "Done"
