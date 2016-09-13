import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import uuid
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class survey:
    """Class for handling intents surveys from google sheets"""

    def __init__(self):
        pass

    def load(self, x):
        try:
            
            self.raw = pd.read_csv(x)
            self.raw['uuid'] = [uuid.uuid4() for x in self.raw.index]

            # Strip whitespace from columns to save problems later!
            
            self.raw.columns = self.raw.columns.str.strip()
            
        except Exception as e:
            return('Error loading raw data from file ' + x)
            print('Original error message:')
            print(repr(e))

        # Define mappings and columns used in iterators

        # Clean date columns
    
    def clean(self):

        self.data = self.raw.copy()

        # Use mapping to rename and subset columns

        self.data.rename(columns = self.mapping, inplace=True)

	# Subset columns mentioned in mapping dict

        cols = list(self.mapping.values())
        self.data = self.data[cols]

        # Arrange date features

        self.data['StartDate'] = clean_startdate(self.data['StartDate'])
        
        self.data = pd.concat(
            [date_features(self.data['StartDate']), self.data],
            axis = 1
        )

        # Features on column names
        try:
            for col in self.data.columns:
                if col in self.categories:
                    self.data[col] = clean_category(self.data[col])
                elif 'comment' in col:
                    self.data[col + '_capsratio'] = [string_capsratio(x) for x in self.data[col]]
                    self.data[col + '_nexcl'] = [string_nexcl(x) for x in self.data[col]]
                    self.data[col + '_len'] = string_len(self.data[col])
                    self.data[col] = clean_comment(self.data[col])
                elif col in self.codes:
                    self.data[col] = clean_code(self.data[col], self.code_levels)
                    
        except Exception as e:
            print('Error cleaning ' + col + ' column')
            print(
            'Note that an error here probably signifies that the subset ',
            'method will not work. Remove problem columns from selection ',
            'before continuing to subset.'
                 )
            print(repr(e))

    # Define code to encode to true (defualt to ok)

    def trainer(self, classes = None):

        if classes == None:
            classes = ['ok']
            
        try:

            self.cleaned = self.data.copy()
            self.cleaned = self.data[self.selection + self.codes]
            self.cleaned = self.cleaned.dropna(how = 'any')
            
            # There is an argument for doing this in the .clean() method.
            # It might useful to be able to call the data before this is
            # applied however. Note that after running load(), clean(),
            # rainer() there are now three similar copies of the data being
            # stored within the class object. At the present small scale this
            # is not a problem, but in time it may be necessary to readress 
            # this.
            
            # LabelEncoder converts labels into numeric codes for all of the factors.

            le = LabelEncoder()

            for col in self.categories:
                self.cleaned.loc[:,col] = le.fit_transform(self.cleaned.loc[:,col])
            
            le.fit(self.cleaned['code1'])
            self.cleaned['code1'] = le.transform(self.cleaned['code1'])

            # At present this deals only with the binary case. Would be
            # good to generalise this in future to allow it to be customised.
            # This codes the outcomes as 0 or 1, but ideall would do 0, 1, 2, etc.

            self.bin_true = le.transform(classes)

            self.cleaned['code1'] = [1 if x in self.bin_true else 0 for x in self.cleaned['code1']] 

            #self.cleaned.loc[self.cleaned['code1'] not in self.bin_true,'code1'] = 0
            #self.cleaned.loc[self.cleaned['code1'] in self.bin_true,'code1'] = 1

        except Exception as e:
            print('There was an error while running trainer method')
            print('Original error message:')
            print(repr(e))

    def predictor(self):

        try:

            self.cleaned = self.data.copy()
            self.cleaned = self.data[self.selection]
            self.cleaned = self.cleaned.dropna(how = 'any')

# Debug            print(self.cleaned.isnull().sum())

            le = LabelEncoder()

            for col in self.categories:
                self.cleaned.loc[:,col] = le.fit_transform(self.cleaned.loc[:,col])

        except Exception as e:
            print('There was an error while subsetting survey data')
            print('Original error message:')
            print(repr(e))

    mapping = {
        'uuid': 'uuid',
        'Respondent ID':'Respondent_ID',
        'Start Date':'StartDate',
        'Page':'page',
        'Org':'org',
        'Section':'section',
        'Work or Personal':'cat_work_or_personal',
        'What work?':'comment_what_work',
        'Satisfaction':'cat_satisfaction',
        'Describe Why You Came Today':'comment_why_you_came',
        'Satisfaction Comment, Describe Why You Came Today, Further comments':'comment_why_you_came_satisfaction',
        'Found?':'cat_found_looking_for',
        'Other (Found What)':'comment_other_found_what',
        'Help?':'cat_anywhere_else_help',
        'Other (Elsewhere For Help)':'comment_other_else_help',
        'Where did you go for help?':'comment_where_for_help',
        'Other (Elsewhere For Help), Where did you go for help?':'comment_other_where_for_help',
        'Further comments':'comment_further_comments',
        'CODE':'code1',
    }
    
    categories = [
        # May be necessary to include date columns at soem juncture  
        #'weekday', 'day', 'week', 'month', 'year', 
        'org', 'section', 'cat_work_or_personal', 
        'cat_satisfaction', 'cat_found_looking_for', 
        'cat_anywhere_else_help'
    ]

    comments = [
        'comment_what_work', 'comment_why_you_came', 'comment_other_found_what',
        'comment_other_else_help', 'comment_other_where_for_help', 'comment_where_for_help',
        'comment_why_you_came_satisfaction', 'comment_further_comments'
    ]
    
    codes = [
        'code1'
    ]
    
    # Could do some fuzzy matching here to improve matching to category names
    # Some training examples are likely to be lost in clean_codes due to
    # inconsistent naming of classes by volunteers.
    
    code_levels = [
    'ok', 'finding-general', 'service-problem', 'contact-government', 
    'check-status', 'change-details', 'govuk-specific', 'compliment',
    'complaint-government','notify', 'internal', 'pay', 'report-issue',
    'address-problem', 'verify'
    ]

    selection = ['uuid', 'weekday', 'day', 'week', 'month', 'year'] + categories + [(x + '_len') for x in comments] + [(x + '_nexcl') for x in comments] + [(x + '_capsratio') for x in comments]


def string_len(x):
    try:

        x = x.str.strip()
        x = x.str.lower()

        x = x.replace(r'\,\s?\,?$|none\,', 'none', regex=True)
        
        # Convert NaN to 'a'. Then when counted this will
        # be a 1. Whilst not 0, any entry with 1 is virtually
        # meaningless, so 1 is a proxy for 0.
        
        x = pd.Series([len(y) for y in x.fillna('a')])
        # Now normalise the scores
        
        x = (x - x.mean()) / (x.max() - x.min())
               
    except Exception as e:
        print('There was an error converting strings to string length column!')
        print('Original error message:')
        print(repr(e))
    return(x)

def string_capsratio(x):
    try:
        if not pd.isnull(x):
            x = sum([i.isupper() for i in x])/len(x)
        else:
            x = 0

    except Exception as e:
        print('There was an error creating capitals ratio on column: ' + x)
        print('Original error message:')
        print(repr(e))
    return(x)

def string_nexcl(x):
    try:
        if not pd.isnull(x):
            x = sum([i == '!' for i in x]) / len(x)
        else:
            x = 0

    except Exception as e:
        print('There was an error creating n of exclamations on column: ' + x)
        print('Original error message:')
        print(repr(e))
    return(x)
    
def clean_startdate(x):
    try:
        x = pd.to_datetime(x)
               
    except Exception as e:
        print('There was an error cleaning the StartDate column!')
        print('Original error message:')
        print(repr(e))
    return(x)

def date_features(x):
    try:
        x = pd.to_datetime(x)
        
        X = pd.DataFrame({
                'weekday' : x.dt.weekday,
                'day' : x.dt.day,
                'week' : x.dt.week,
                'month' : x.dt.month,
                'year' : x.dt.year,
             })
        
    except Exception as e:
        print('There was an error creating date feature: ' + x)
        print('Original error message:')
        print(repr(e))
    return(X)

def clean_category(x):
    try:
        
        # May be needed if columns are integer
        x = x.apply(str)
        x = x.str.lower()
        x = x.replace(r'null|\#Value\!', 'none', regex=True)
        x = x.fillna('none')
        x = pd.Series(x)
        x = x.astype('category')
        
    except Exception as e:
        print('There was an error cleaning the', x ,'column.')
        print('Original error message:')
        print(repr(e))
    return(x)

def clean_comment(x):
    try:
        
        x = x.str.strip()
        x = x.str.lower()
        
        # Weirdness with some columns being filled with just a comma.
        # Is this due to improper handling of the csv file somewhere?        
        
        x = x.replace(r'\,\s?\,?$|none\,', 'none', regex=True)
        x = x.fillna('none')
        
    except Exception as e:
        print('There was an error cleaning the', x ,'column.')
        print('Original error message:')
        print(repr(e))
    return(x)
      
def clean_code(x, levels):
    try:

       # If the whole column is not null
       # i.e. we want to train rather than just predict

        if not pd.isnull(x).sum() == len(x):        
            x = x.str.strip()
            x = x.str.lower()
            x = x.replace('\_', '\-', regex=True)
        
            # Rules for fixing random errors.
            # Commented out for now 

            #x = x.replace(r'^k$', 'ok', regex=True)
            #x = x.replace(r'^finding_info$', 'finding_general', regex=True)
            #x = x.replace(r'^none$', np.nan, regex=True)
        
            x[~x.isin(levels)] = np.nan
            x = pd.Series(x)
            x = x.astype('category')
        
    except Exception as e:
        print('There was an error cleaning the', x ,'column.')
        print('Original error message:')
        print(repr(e))
    return(x)

# Below copied from Tom Ewings LDA notebook

stops = set(stopwords.words("english"))     # Creating a set of Stopwords
p_stemmer = PorterStemmer() 

def concat_ngrams(x):
    #if len(x) > 1 & isinstance(x, list):
    if isinstance(x, tuple):
        x = '_'.join(x)
    return(x)

def cleaner(row):
    
    # Function to clean the text data and prep for further analysis
    text = row.lower()                      # Converts to lower case
    text = re.sub("[^a-zA-Z]"," ",text)          # Removes punctuation
    text = text.split()                          # Splits the data into individual words 
    text = [w for w in text if not w in stops]   # Removes stopwords
    text = [p_stemmer.stem(i) for i in text]     # Stemming (reducing words to their root)
    text3 = list(ngrams(text, 2))
    text2 = list(ngrams(text, 3))
    text = text + text2 + text3
    text = list([concat_ngrams(i) for i in text])
    
    return(text)  
