# The GUI and model implementation code for ML Project-3 Team 37
"""============================== AUTHOR: PIYUSH PRADEEP TERKAR ====================================================="""
# importing all the libraries
from tkinter import *
import matplotlib.pyplot as plt
import nltk
import pandas as pd

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

# creating all objects beforehand so that they have a global scope
cv = CountVectorizer(max_features=1500)
wl = WordNetLemmatizer()
all_stopwords = set(stopwords.words('english')) - {'not', 'but', 'nasty', 'great', 'bad', 'good', 'wasted'}
all_stopwords.add('place')
all_stopwords.add('restaurant')
all_stopwords.add('food')
all_stopwords.add('hotel')

from sklearn.decomposition import PCA

pca = PCA(n_components=100)


# function definitions


def userinput(inputdata):
    """ This function accepts the user input and converts it into numeric data ready to feed to the model
        param: String data as the parameter inputdata
        returns: A matrix containing the numeric code for inputdata"""
    # remove all the punctuations
    re.sub('^a-zA-Z', ' ', inputdata)
    # now convert this to lowercase
    inputdata.lower()
    # create a list of words for review
    inputdata = inputdata.split()
    # convert all the words to their basal form, using PortStemmer object
    # collect all the stopwords from english language to compare them
    # create a list of important words now
    inputdata = [wl.lemmatize(word) for word in inputdata if word not in set(all_stopwords)]
    # now again convert this list to a String of required words
    inputdata = ' '.join(inputdata)
    cv.fit_transform(vocabularyOfModel)
    inputdata = cv.transform([inputdata])
    return inputdata


def model(inputdata):
    """This function is the actual NLP model,****THE CODE FOR OUR MODEL GOES INSIDE THIS FUNCTION*****,
    its only parameter is inputdata which is the matrix returned from the userinput function
    param: String returned from the userinput function
    returns: An integer 0 or 1 which is predicted by the model"""
    global vocabularyOfModel
    corpus = vocabularyOfModel
    x = cv.fit_transform(corpus).toarray()
    print(len(x))
    y = df.iloc[:, -1].values
    # split the data into train and test set
    from sklearn.model_selection import train_test_split
    x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.01, random_state=25)
    # ---------------------------------------------K-NearestNeighbors Algorithm-----------------------------------------
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors=1, algorithm='brute')
    # fit the model
    classifier.fit(x_tr, y_tr.ravel())
    y_pred = classifier.predict(x_te)
    # accuracy score and confusion matrix
    from sklearn.metrics import accuracy_score, confusion_matrix, plot_confusion_matrix
    print(accuracy_score(y_te, y_pred))
    print(confusion_matrix(y_te, y_pred))
    plot_confusion_matrix(estimator=classifier, X=x_tr, y_true=y_tr)
    plt.show()
    result = classifier.predict(inputdata)
    return result


def opennewwindow(inputdata, chk):
    """This function takes user input to find if the prediction was write
        if the prediction is found wrong the improve function is called"""
    # Toplevel object which will
    # be treated as a new window
    newwindow = Toplevel(tk)

    # sets the title of the
    # Toplevel widget
    newwindow.title("Help us Improve")

    # sets the geometry of toplevel
    newwindow.geometry("500x200")

    # A Label widget to show in toplevel
    Label(newwindow,
          text="Was the guess correct?\n The guess is presented on the main window in red colour text", font=26).pack()
    Button(newwindow, text="Yes", font=largefont, command=lambda: newwindow.destroy()).pack(side=LEFT, padx=20, pady=10)
    Button(newwindow, text="No", font=largefont, command=lambda: improve(inputdata, chk=chk, instance=newwindow)) \
        .pack(side=RIGHT, padx=20, pady=10)


def improve(inputdata, chk, instance):
    """This function takes the input review and appends it to the data set"""
    import csv
    with open('Restaurant_Reviews.tsv', 'at') as out_file:
        # create a writer object to append to the data set
        tsv_writer = csv.writer(out_file, delimiter='\t')
        # set the right value of 'label'
        if chk == 1:
            # append the correct value to dataset
            tsv_writer.writerow([inputdata, '0'])
        else:
            tsv_writer.writerow([inputdata, '1'])
    instance.destroy()


def onclick():
    """This fuction is called upon clicking the give review button in th ui, it has no parameters
    it returns the result of the review by calling the userinput function and passing it's return value to the model
    function
    params: None
    returns: None
    input: none
    output: String output, result whether the review is positive or negative"""
    if e.get() != emptyString:
        if model(inputdata=userinput(emptyString + e.get())) == 1:
            # pass the inputdata to userinput and model function to check if value is 1
            result = "Thank you for such a Positive feedback, visit again!"
            chk = 1
        else:  # if the value is not one print the following
            result = "We will improve ourselves, sorry for inconvinince"
            chk = 0
        textoutput.set(result)  # print the result on the gui
        opennewwindow(inputdata=emptyString + e.get(), chk=chk)
        textinput.set("")  # after the input is complete clear the textfield/textbox (known as Entry) for fresh input
    else:
        textoutput.set("Please type something")


# -------------------------------------- creating the vocabulary--------------------------------------------------------
# import the data-set
df = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
# bag of worlds model
import re
import nltk

nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

vocabularyOfModel = []
for i in range(0, len(df['Review'])):
    review = df['Review'][i]  # accessing the ith review
    # remove all the punctuations
    re.sub('^a-zA-Z', ' ', review)
    # now convert this to lowercase
    review.lower()
    # create a list of words for review
    review = review.split()
    # convert all the words to their basal form, using WordNetLementizer object
    wl = WordNetLemmatizer()
    # get all the words and remove all the stopwords from the data
    all_stopwords = set(stopwords.words('english')) - {'not', 'but', 'is', 'the', 'nasty', 'great', 'bad', 'good'}
    # collect all the stopwords from english language to compare them
    # create a list of important words now
    review = [wl.lemmatize(word) for word in review if word not in set(all_stopwords)]
    # now again convert this list to a String of required words and append it to corpus
    review = ' '.join(review)
    vocabularyOfModel.append(review)

# GUI code
tk = Tk()  # creating the gui object
largefont = ('Verdana', 30)  # font style and size for output
tk.title("Restaurant Review")  # Title of the window
bgimage = PhotoImage(file='vector-flat-restaurant-01.png')  # Background image
background = Label(tk, image=bgimage)  # setting the background image
background.place(x=0, y=0, relwidth=1, relheight=1)  # parameters to set the image
tk.minsize(1000, 500)  # the minimum size of the window below which the window can't be resized
emptyString = ""  # a string to store the inputdata
textoutput = StringVar()  # textvariable objects to access and edit the contents within th Entry
textinput = StringVar()  # textvariable object for output
textinput.set(emptyString)  # setting the emptyString in the Entry when rendering the gui
textoutput.set("")  # setting the output label as empty when rendering the gui
e = Entry(tk, textvariable=textinput)  # Entry - this is where the user types input in the model
e.pack(fill=X, padx=20, pady=10)  # parameters on how to display the Entry

# button and it's parameters and the function to be called when it is clicked
giveReviewButton = Button(tk, text="Give Review", background='white', command=lambda: onclick()).pack()

# The output label which displays the output for the review stating weather it was positive or not
resultLabel = Label(tk, textvariable=textoutput, font=largefont, bg='sky blue', fg='red')
resultLabel.pack()
# an instruction label to guide the user while using the gui
instructionLabel = Label(tk, text="Enter a meaningful review in English language,\n our Machine Learning code will " +
                                  "predict the sentiment as positive or negative\n" +
                                  "Neutral reviews will be treated as negative", bg='sky blue')
instructionLabel.pack()
# the mainloop function which is called so that the gui can be executed
tk.mainloop()
