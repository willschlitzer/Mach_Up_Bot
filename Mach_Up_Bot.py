import praw
import Mach_Up_Bot_config
import time
import datetime
import random


def logger(x):
    with open ('Mach_Up_Bot_running_info.txt','a') as f:
        f.write('Mach Up Bot,' + x + ',')
        f.write (str(datetime.datetime.now()) + '\n')
    #print ("Mach Up Bot, " + x + ',' + str(datetime.datetime.now()))

def bot_login():
    r = praw.Reddit(username = Mach_Up_Bot_config.username,
            password = Mach_Up_Bot_config.password,
            client_id = Mach_Up_Bot_config.client_id,
            client_secret = Mach_Up_Bot_config.client_secret,
            user_agent = "/u/Bahet")
    return r

def get_story():
    number = random.randint(1,3)
    if number == 1:
        with open ("Ground_Speed_Check.txt","r") as f:
            story = f.read()
    if number == 2:
        #with open ("Blackbird_Flyby.txt","r") as f:
            #story = f.read()
        number = 3
    if number == 3:
        with open ("SAM_Outrun.txt","r") as f:
            story = f.read()
    return story

def run_bot(r, comments_replied_to, submissions_replied_to, sublist):
    titlenumber = 500
    commentnumber = 10000
    sublist = ['airforce', 'aviation', 'militaryporn', 'military', 'history', 'space']
    #sublist = ['aviation']
    for sub in sublist:
        for submission in r.subreddit(sub).new(limit=titlenumber):
            text = str(submission.title)
            text = str.upper(text)
            if 'SR-71' in text or 'SR71' in text:
                if submission.id not in submissions_replied_to and not submission.author == r.user.me():
                    mycomment = get_story()
                    #print (mycomment)
                    #print ('Submission hit')
                    submission.reply(mycomment)
                    submissions_replied_to.append(submission.id)
                    with open ("Mach_Up_Bot_submissions_replied_to.txt","a") as f:
                        f.write(submission.id+"\n")
                    with open ("Mach_Up_Bot_reply_data.txt", "a") as f: 
                        f.write ('Submission,')
                        f.write (str(submission.author) + ',')
                        f.write (str(submission.id) +',')
                        f.write (str(sub + ','))
                        f.write (str(datetime.datetime.now()) + '\n')     
        for comment in r.subreddit(sub).comments(limit=commentnumber):
            text = str(comment.body)
            text = str.upper(text)
            if 'SR-71' in text or 'SR71' in text:
                if comment.id not in comments_replied_to and not comment.author == r.user.me():
                    if str.upper("Roger that Aspen") not in text and str.upper("myriad of sophisticated navigation") not in text:
                        mycomment = get_story()
                        #print (mycomment)
                        print ('Comment hit')
                        comment.reply(mycomment)
                        comments_replied_to.append(comment.id)
                        with open ("Mach_Up_Bot_comments_replied_to.txt","a") as f:
                            f.write(comment.id+"\n")
                        with open ("Mach_Up_Bot_reply_data.txt", "a") as f: 
                            f.write ('Comment,')
                            f.write (str(comment.author) + ',')
                            f.write (str(comment.id) +',')
                            f.write (str(sub + ','))
                            f.write (str(datetime.datetime.now()) + '\n')
        print ('r/' + sub)

def get_saved_comments():
    with open("Mach_Up_Bot_comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
    return comments_replied_to

def get_saved_submissions():
    with open("Mach_Up_Bot_submissions_replied_to.txt", "r") as f:
        submissions_replied_to = f.read()
        submissions_replied_to = submissions_replied_to.split("\n")
    return submissions_replied_to

def reddit_logger(r):
    for submission in r.subreddit('BahetBotTest').new(limit=100):
        if submission.id == '6iu00z':
            submission.reply("Mach Up Bot Cycle Complete")
            #print ('Posted to Reddit')

def get_sublist():
    with open("Mach_Up_Bot_sublist.txt","r") as f:
        sublist = f.read()
        sublist = sublist.split("\n")
        return sublist

def main():
    #logger("Start")
    r = bot_login()
    sublist = get_sublist()
    comments_replied_to = get_saved_comments()
    submissions_replied_to = get_saved_submissions()
    run_bot(r, comments_replied_to, submissions_replied_to, sublist)
    #time.sleep(120)
    #reddit_logger(r)
    #logger("End")

#while True:
 #  main()
main()    
