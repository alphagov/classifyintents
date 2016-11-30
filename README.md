[![GitHub tag](https://img.shields.io/github/tag/ivyleavedtoadflax/classify.svg)]()

# classify

This is a python module for use with the GOV.UK intent survey classification by machine learning algorithm.
The module contains the `classify.survey` class which cleans and prepares the data for machine learning.

Since v0.4.0 this module should be installed as a module using the line `git+git://github.com/ivyleavedtoadflax/classify.git` in your `requirements.txt` file, and the command `pip install -r requirements.txt`.

## Requirements

* Python >= 3.5 
See `requirements.txt`

## Usage

### Loading data

To begin instantiate an instance of the class with:

```
import survey from classify

intent = survey()
```

Load some raw data.
The class expects an unedited CSV file downloaded from survey monkey.
Note that the `load()` method also does some cleaning of the column names, 
nd drops a row from the csv files which includes a sub heading pertaining to question types that is included by survey monkey

```
intent.load('data.csv')
```

The data is stored as pandas dataframe in the class named `intent.raw`.

### Cleaning the raw data

The next step is to perform some cleaning of the raw data.
This is accomplished in the `clean_raw()` method.
This method does a number of things:

* Creates a copy of the `intent.raw` dataframe, and calls this new dataframe `intent.data`.
* The messy column names inherited are cleaned up using a dictionary called `intent.raw_mapping`.
    * Note that if the format of the survey or the names of questions are changed, breaking the class, a quick fix may be to ensure that the `intent.raw_mapping` dictionary continues to make sense.
* A number of new features are added to the data:
    * Time taken to complete the survey
    * Some simple features based on the free text
        * Number of characters in the string.
        * Ratio of capital letters exclamation marks to total number of characters.

### Determining the org and section

The page that the user was visiting when they were asked to complete the survey is recorded in a cleaned field called `full_url`.
In this step the URLs are cleaned according to a number of rules, and then the unique URLs are extracted and then queried using the GOV.UK content API.
This returns an organisation (`org`) and a section (`section`).

These data are then merged back into the `intent.data` dataframe.
This step is completed with:

```
intent.api_lookup()
```

This step is verbose, and can take a while if there are a large number of URLs to lookup.

### Preparing the data from training or prediction

Assuming all has gone well so far, the next step is to prepare the data for training or prediction using a machine learnign algorithm.
This is done with the methods `intent.trainer()` and `intent.predictor()` respectively.

When calling `intent.trainer()` a list of classes must be passed as an argument.
As part of the method, all classes that are not specified in the list are concatenated into one, enabling one-versus-all (OVA) classification.

Using the `predictor()` method will remove the outcome class, if it was present.


