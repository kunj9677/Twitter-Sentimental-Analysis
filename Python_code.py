import re, sys, csv
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        #auth
        consumerKey = 'XXXXXXXXXXXXXXXXX'
        consumerSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accessToken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accessTokenSectet = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
        auth.set_access_token(accessToken,accessTokenSectet)
        api = tweepy.API(auth)

        #user_input
        searchT = input("Enter KeyWord : ")
        noOfTweets = int(input("Enter No of Tweets : "))

        #seach
        self.tweets = tweepy.Cursor(api.search_tweets, q = searchT,lang="en").items(noOfTweets)

        #file handle
        csvFile = open('data.csv','a')

        csvWriter = csv.writer(csvFile)

        #  -1 to 1

        """ 

            -1 to 0 to 1

            0-->n
            0 to 0.3---->wp
            0.3 to 0.6 --->p
            0.6 to 1 ----->sp
            -0.3 to 0 -> wn
            -0.3 to -0.6 -> n
            -0.6 to -1 ->sn

        """
        #data_store_reset
        neutral = 0
        wpostive = 0
        positive = 0
        spositive = 0
        wnegative = 0
        negative = 0
        snegative = 0

        for tweet in self.tweets:
            self.tweetText.append(self.cleanText(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)

            polarity = analysis.sentiment.polarity
            polarity += polarity

            if(analysis.sentiment.polarity == 0):
                neutral +=1
            elif(analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpostive +=1
            elif(analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive +=1
            elif(analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <=1 ):
                spositive +=1
            elif( analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative +=1
            elif(analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative +=1
            elif(analysis.sentiment.polarity >-1 and analysis.sentiment.polarity <=-0.6):
                snegative +=1 

        csvWriter.writerow(self.tweetText)
        csvFile.close()

        positive = self.percentage(positive,noOfTweets)
        wpostive = self.percentage(wpostive,noOfTweets)
        spositive = self.percentage(spositive,noOfTweets)
        wnegative = self.percentage(wnegative,noOfTweets)
        negative = self.percentage(negative,noOfTweets)
        snegative = self.percentage(snegative,noOfTweets)
        neutral = self.percentage(neutral,noOfTweets)
        
        polarity = polarity/noOfTweets

        print("People reaction on "+searchT+ " out of "+str(noOfTweets)+" tweets.")
        
        print()

        print("Report :")

        if(polarity == 0):
            print("neutral")
        elif(polarity > 0 and polarity <=0.3):
            print("weakly positive")
        elif(polarity > 0.3 and polarity <=0.6):
            print("positive")
        elif(polarity > 0.6 and polarity <=1):
            print("strong positive")
        elif(polarity > -0.3 and polarity <=0):
            print("weakly negative")
        elif(polarity > -0.6 and polarity <=-0.3):
            print("negative")
        elif(polarity > -1 and polarity <=-0.6):
            print("strong negative")

        print()
        print("Report with values :")

        print(str(positive)+" % people are +ve ")
        print(str(wpostive)+" % people are weakly +ve ")
        print(str(spositive)+" % people are strong +ve ")
        print(str(wnegative)+" % people are weakly -ve ")
        print(str(negative)+" % people are -ve ")
        print(str(snegative)+" % people are strong -ve ")
        print(str(neutral)+" % people are neutral")

        self.plotPieChart(positive,wpostive,spositive,wnegative,negative,snegative,neutral,searchT,noOfTweets)



    def cleanText(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)"," ",tweet).split())
    
    def percentage(self,part,total) :
        count = 100 * float(part) / float(total)
        return format(count,'.2f')

    def plotPieChart(self,positive,wpostive,spositive,wnegative,negative,snegative,neutral,searchT,noOfTweets):
        labels = [
            'Positive '+str(positive)+' %',
            'Wekly Positive '+str(wpostive)+' %',
            'Strongly Positive '+str(spositive)+' %',
            'Neutral '+str(neutral)+' %',
            'Negative '+str(negative)+' %',
            'Wekly Negative '+str(wnegative)+' %',
            'Strongly Negative '+str(snegative)+' %',
        ]
        sizes = [
            positive,wpostive,spositive,neutral,negative,wnegative,snegative
        ]
        colors = [
            'yellowgreen',
            'lightgreen',
            'darkgreen',
            'darkred',
            'red',
            'lightsalmon',
            'gold'
        ]
        patches, texts = plt.pie(sizes,colors=colors,startangle=90)
        plt.legend(patches,labels,loc="best")
        plt.title("How People are react on "+searchT+" by checking "+str(noOfTweets)+" tweets.")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()





if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()







