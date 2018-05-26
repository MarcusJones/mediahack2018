#%% ===========================================================================
# Standard imports
# =============================================================================
import os
import yaml

#%% ===========================================================================
# Setup logging
# =============================================================================
import logging.config
ABSOLUTE_LOGGING_PATH = r"/home/batman/git/py_ExergyUtilities/LoggingConfig/loggingNoFile.yaml"
ABSOLUTE_LOGGING_PATH = r"/home/batman/git/py_ExergyUtilities/LoggingConfig/loggingSimpleYaml.yaml"
#FILE_CONSOLE_LOGGING_PATH = r"/home/batman/git/py_ExergyUtilities/LoggingConfig/loggingWithFile.yaml"
log_config = yaml.load(open(ABSOLUTE_LOGGING_PATH, 'r'))
logging.config.dictConfig(log_config)
fh = logging.FileHandler(filename=os.path.join(os.getcwd(), 'log.txt'))
fh.setLevel('DEBUG')

FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
FORMAT = "%(asctime)s - %(levelno)-3s - %(module)-10s  %(funcName)-10s: %(message)s"
logformat = logging.Formatter(FORMAT)

fh.setFormatter(logformat)

logging.info("Started logging, configuration from {}".format( os.path.split(ABSOLUTE_LOGGING_PATH)[1]))

#%%
import pandas as pd

#%% ===========================================================================
#  Data source and paths
# =============================================================================
PATH_DATA_ROOT = r"/home/batman/Dropbox/DATA/audio Ryerson/Audio_Speech_Actors_01-24/"
path_data = os.path.join(PATH_DATA_ROOT, r"")
assert os.path.exists(path_data), path_data

#%% Descriptions
#Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
#Vocal channel (01 = speech, 02 = song).
#Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
#Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.
#Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").
#Repetition (01 = 1st repetition, 02 = 2nd repetition).
#Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).

FILE_MAPPING = [
"Modality ", # IGNORE
"Vocal channel",  # IGNORE
"Emotion", # Select only 03, 04, 05
"Emotional intensity", # IGNORE
"Statement", # IGNORE
"Repetition", # IGNORE
"Actor", # Split M/F
        ]

EMOTION_MAP = {'03':'happy',
               '04': 'sad',
               '05': 'angry',
               }

#GENDER_MAP = 
#Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
#Vocal channel (01 = speech, 02 = song).
#Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
#Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.
#Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").
#Repetition (01 = 1st repetition, 02 = 2nd repetition).
#Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).


#Video-only (02)
#Speech (01)
#Fearful (06)
#Normal intensity (01)
#Statement "dogs" (02)
#1st Repetition (01)
#12th Actor (12)
#Female, as the actor ID number is even.

#%% Get all files

def get_files_by_ext_recurse(rootPath,ext, ):
    ext = "." + ext

    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)


    # Filter
    resultFilePaths = list()

    resultFilePaths = [filePath for filePath in allFilePathList if
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]

    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))

    return resultFilePaths

files = get_files_by_ext_recurse(PATH_DATA_ROOT,"wav")

#%% Filter files
entries = list()
#for i,f in enumerate(files[0:10]): 
for i,f in enumerate(files[:]): 
    #print(f)
    this_entry = dict()
    path, fnameext = os.path.split(f)
    fname, ext = os.path.splitext(fnameext)
    fname_vec = fname.split('-')
    
    this_entry = dict(zip(FILE_MAPPING,fname_vec))
    this_entry['file_name'] = fnameext
    logging.info("Processing file {}, {}".format(i,fname))
    
    if this_entry['Emotion'] in EMOTION_MAP.keys():
        this_entry['emotion_label'] = EMOTION_MAP[this_entry['Emotion']]
        
        if int(this_entry['Actor']) % 2 == 1:
            this_entry['gender_label'] = 'Male'
        elif int(this_entry['Actor']) % 2 == 0:
            this_entry['gender_label'] = 'Female'
        logging.info("KEEP {} {}".format(this_entry['emotion_label'], this_entry['gender_label']))
        this_entry['full_path']  = f
        entries.append(this_entry)
    else:
        logging.info("SKIP")
        continue
    
logging.info("{} files entered in database, {} discarded".format(len(entries),len(files) - len(entries)))

#%% Create a DF
df = pd.DataFrame(entries)
out_path = "./Marcus_index.csv"
df.to_csv(out_path)


df['emotion_label'].value_counts()
df['Statement'].value_counts()


#%% ===========================================================================
#  Load Train and Test data
# =============================================================================
logging.info(f"Load train and test")
data_train = pd.read_csv(os.path.join(path_data, "train.zip"),delimiter='\t',compression='zip',index_col='id')
logging.info(f"Loaded {len(data_train)} train rows")

#data_test = pd.read_csv(os.path.join(path_data, "test.csv"),delimiter='\t', )
data_test = pd.read_csv(os.path.join(path_data, "test.zip"),delimiter='\t',compression='zip',index_col='id')
logging.info(f"Loaded {len(data_test)} test rows")

#%% SUBSET; 2 subreddits

# Select a list of categories
selection = ['movies','gaming']

# Empty masks
this_train_filter = np.full(data_train.shape[0],False)
this_test_filter = np.full(data_test.shape[0],False)
for this_category in selection:
    # Concantenate for train
    selected_train_rows = data_train['subreddit'].values == this_category
    this_train_filter = this_train_filter | selected_train_rows
    # Concantenate for test
    selected_test_rows = data_test['subreddit'].values == this_category
    this_test_filter = this_test_filter | selected_test_rows
    logging.debug(f"({np.sum(selected_train_rows)} {np.sum(selected_test_rows)}) (train, test) matches for category: {this_category}")

frac_tr = np.sum(this_train_filter)/len(data_train)*100
frac_te = np.sum(this_test_filter)/len(data_test)*100

logging.info(f"{np.sum(this_train_filter)} train records selected ({frac_tr:{0}.{2}}%) -> Xy_tr")
logging.info(f"{np.sum(this_test_filter)} test records selected ({frac_te:{0}.{2}}%) -> X_te")

Xy_tr   = data_train[this_train_filter] 
X_te    = data_test[this_test_filter]   

#%% DONE HERE - DELETE UNUSED
print("******************************")

del_vars =[
        "data_test",
        "data_train",
        "selected_train_rows",
        "this_train_filter",
        "selected_test_rows",
        "this_test_filter",
        "selection",
        "this_category",
        "path_data",
        "frac_tr",
        "frac_te",
        "",
        "",
        #"In",
        #"Out",
        
        ]
cnt = 0
for name in dir():
    if name in del_vars:
        cnt+=1
        del globals()[name]
logging.info(f"Removed {cnt} variables from memory")
del cnt, name, del_vars
#%%
#
#keep_vars =[
#        "keep_vars",
#        "Xy_tr",
#        "X_te",
#        "In",
#        "Out",
#        
#        ]
#for name in dir():
#    print(name, end=" ")
#    if name.startswith('__'):
#        print("keep")
#        pass
#    if name.startswith('_'):
#        print("keep")
#        pass    
#    elif name in keep_vars:
#        print("keep")
#        pass
#    else:
#        print("del")
#        del globals()[name]
#    
#raise







