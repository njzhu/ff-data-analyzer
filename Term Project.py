from cmu_112_graphics import *
import tkinter as tk
import bs4, requests
from bs4 import BeautifulSoup, SoupStrainer
import math
import string
import matplotlib.pyplot as plt

class MyApp(App):
    def appStarted(self):
        self.accuracies = []
        self.binaries = []
        self.Sean = Analyst('Sean Koerner')
        self.Justin = Analyst('Justin Boone')
        self.Jason = Analyst('Jason Moore')
        self.Andy = Analyst('Andy Holloway')
        self.Mike = Analyst('Mike Wright')
        self.Tags = Analyst('Mike Tagliere')
        self.Pat = Analyst('Pat Fitzmaurice')
        url3 = 'https://x360wallpapers.files.wordpress.com/2010/05/madden-nfl-2010_nxebg.jpg'
        self.image1 = self.loadImage(url3)
        urlback = 'https://avante.biz/wp-content/uploads/Nfl-Wallpaper/Nfl-Wallpaper-066.jpg'
        self.imageback = self.loadImage(urlback)
        self.first1 = ''
        self.last1 = ''
        self.first2 = ''
        self.last2 = ''
        shade = False
        self.colorstart = 'red'
        self.clickStart = False
        self.clickOptions = False
        self.clickOptions2 = False
        self.clickOptions3 = False
        self.onBlock1 = False
        self.onBlock2 = False
        self.onBlock3 = False
        self.onBlock4 = False
        self.onQB = False
        self.onRB = False
        self.onWR = False
        self.onTE = False
        self.onPlayer = False
        self.onTeam = False
        self.block2clicked = False
        self.block3clicked = False
        self.block4clicked = False
        self.qbClicked = False
        self.rbClicked = False
        self.wrClicked = False
        self.teClicked = False
        self.clickPlayer = False
        self.clickTeam = False
        self.options = ''
        self.scoreOptions = ['PPR', 'HALF-PPR', 'Standard']
        self.qbOptions = ['1 QB', '2 QB/Superflex']
        self.qbScoroptions = ['4pt TD', '6pt TD']
        self.position = 0
        self.onRedo = False
        self.redoClicked = False
        # [QB, RB1, RB2, WR1, WR2, TE]
        self.teamWeights = [0.23, 0.17, 0.15, 0.21, 0.15, 0.9]
        self.teamTotal = sum(self.teamWeights)
        self.Sean.extractWeights()
        self.Justin.extractWeights()
        self.Jason.extractWeights()
        self.Andy.extractWeights()
        self.Mike.extractWeights()
        self.Pat.extractWeights()
        self.team1 = []
        self.team2 = []
        self.onJason = False
        self.onAndy = False
        self.onMike = False
        self.onPat = False
        self.onSubmit = False

    def splitName(self, name1):
        name1 = name1.lower()
        tuple1 = name1.split(" ")
        first1, last1 = tuple1[0], tuple1[1]
        return first1, last1

    def getUrl(self, name1, name2):
        # https://www.fantasypros.com/nfl/start/aaron-rodgers-patrick-mahomes.php
        name1 = name1.lower()
        name2 = name2.lower()
        tuple1 = name1.split(" ")
        tuple2 = name2.split(" ")
        first1, last1 = tuple1[0], tuple1[1]
        first2, last2 = tuple2[0], tuple2[1]
        url = f'https://www.fantasypros.com/nfl/start/{first1}-{last1}-{first2}-{last2}.php?scoring={self.options}'
        #print(url)
        return url

    def getNames(self, name1, name2):
        name1 = name1.lower()
        name2 = name2.lower()
        # method taken from https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
        name1 = name1.translate(str.maketrans('', '', string.punctuation))
        name2 = name2.translate(str.maketrans('', '', string.punctuation))
        tuple1 = name1.split(" ")
        tuple2 = name2.split(" ")
        first1, last1 = tuple1[0], tuple1[1]
        first2, last2 = tuple2[0], tuple2[1]
        #self.first1, self.last1 = first1, last1
        #self.first2, self.last2 = first2, last2
        return first1, last1, first2, last2

    def mouseMoved(self, event):
        if (self.width/2-100 <= event.x <= self.width/2 + 100) and \
            (self.height/2-30 <= event.y <= self.height/2 + 30) and \
            self.clickStart == False:
            self.onBlock1 = True
        elif (150 <= event.x <= 350) and (200 <= event.y <= 400) and \
            self.clickStart == True:
            self.onBlock2 = True
        elif (150 <= event.x <= 350) and (450 <= event.y <= 650) and \
            self.clickStart == True:
            self.onBlock3 = True
        elif (150 <= event.x <= 350) and (700<= event.y <= 900) and \
            self.clickStart == True:
            self.onBlock4 = True
        elif (650 <= event.x <= 850) and (325 <= event.y <= 375) and \
            self.clickStart == True:
            self.onQB = True
        elif (650 <= event.x <= 850) and (425 <= event.y <= 475) and \
            self.clickStart == True:
            self.onRB = True
        elif (950 <= event.x <= 1150) and (325 <= event.y <= 375) and \
            self.clickStart == True:
            self.onWR = True
        elif (950 <= event.x <= 1150) and (425 <= event.y <= 475) and \
            self.clickStart == True:
            self.onTE = True
        elif (800 <= event.x <= 1000) and (650 <= event.y <= 700) and \
            self.clickStart == True:
            self.onPlayer = True
        elif (800 <= event.x <= 1000) and (750 <= event.y <= 800) and \
            self.clickStart == True:
            self.onTeam = True
        elif (1450 <= event.x <= 1650) and (350 <= event.y <= 400) and \
            self.clickStart == True:
            self.onJason = True
        elif (1450 <= event.x <= 1650) and (450 <= event.y <= 500) and \
            self.clickStart == True:
            self.onAndy = True
        elif (1450 <= event.x <= 1650) and (550 <= event.y <= 600) and \
            self.clickStart == True:
            self.onMike = True
        elif (1450 <= event.x <= 1650) and (650 <= event.y <= 700) and \
            self.clickStart == True:
            self.onPat = True
        elif (self.width/2 - 50 <= event.x <= self.width/2 + 50) and (self.height - 100 <= event.y <= self.height-50) and self.clickStart == True:
            self.onSubmit = True
        # 1500, 900, 1800, 1080
        elif (1500 <= event.x <= 1800) and (900 <= event.y <= 1080) and \
            self.clickOptions == True:
            self.onRedo = True
        else: 
            self.onBlock1 = False
            self.onBlock2 = False
            self.onBlock3 = False
            self.onBlock4 = False
            self.onQB = False
            self.onRB = False
            self.onWR = False
            self.onTE = False
            self.onPlayer = False
            self.onTeam = False
            self.onRedo = False
            self.onJason = False
            self.onAndy = False
            self.onMike = False
            self.onPat = False
            self.onSubmit = False

    def getSettings(self):
        if self.block2clicked:
            self.options = 'PPR'
        elif self.block3clicked:
            self.options = 'HALF'
        else:
            self.options = 'STD'
        return self.options

    def mousePressed(self, event):
        if (self.width/2-100 <= event.x <= self.width/2 + 100) and \
            (self.height/2-30 <= event.y <= self.height/2 + 30):
            self.clickStart = True
        elif 150 <= event.x <= 350 and 200 <= event.y <= 400 and self.clickStart == True:
            self.block2clicked = not self.block2clicked
            self.block3clicked = False
            self.block4clicked = False
        elif (150 <= event.x <= 350) and (450 <= event.y <= 650) and self.clickStart == True:
            self.block3clicked = not self.block3clicked
            self.block2clicked = False
            self.block4clicked = False
        elif (150 <= event.x <= 350) and (700<= event.y <= 900) and self.clickStart == True:
            self.block4clicked = not self.block4clicked
            self.block2clicked = False
            self.block3clicked = False
        # 500, 325, 700, 375
        elif (650 <= event.x <= 850) and (325 <= event.y <= 375) and self.clickStart == True:
            self.position = 0
            self.qbClicked = not self.qbClicked
            self.rbClicked = False
            self.wrClicked = False
            self.teClicked = False
        # 500, 425, 700, 475
        elif (650 <= event.x <= 850) and (425 <= event.y <= 475) and self.clickStart == True:
            self.position = 1
            self.rbClicked = not self.rbClicked
            self.qbClicked = False
            self.wrClicked = False
            self.teClicked = False
        # 750, 325, 950, 375
        elif (950 <= event.x <= 1150) and (325 <= event.y <= 375) and self.clickStart == True:
            self.position = 2
            self.wrClicked = not self.wrClicked
            self.qbClicked = False
            self.rbClicked = False
            self.teClicked = False
        # 750, 425, 950, 475
        elif (950 <= event.x <= 1150) and (425 <= event.y <= 475) and self.clickStart == True:
            self.position = 3
            self.teClicked = not self.teClicked
            self.qbClicked = False
            self.rbClicked = False
            self.wrClicked = False
        # 625, 750, 825, 800
        elif (800 <= event.x <= 1000) and (750 <= event.y <= 800) and self.clickStart == True:
            self.accuracies = []
            self.binaries = []
            self.condition = 2
            self.clickTeam = not self.clickTeam
        # 625, 650, 825, 700
        elif (800 <= event.x <= 1000) and (650 <= event.y <= 700) and self.clickStart == True:
            self.accuracies = []
            self.binaries = []
            self.condition = 1
            self.clickPlayer = not self.clickPlayer
        elif (self.width/2 - 50 <= event.x <= self.width/2 + 50) and (self.height - 100 <= event.y <= self.height-50) and self.clickStart == True:
            if self.condition == 1:
                self.getSettings()
                self.clickOptions = True
                self.clickPlayer = False
                self.doPlayer()
            if self.condition == 2:
                self.clickTeam = False
                self.clickPlayer = True
                self.clickOptions = True
                self.getSettings()
                self.doTeam()
        # 1500, 900, 1800, 1080
        elif (1500 <= event.x <= 1800) and (900 <= event.y <= 1080) and self.clickOptions == True:
            self.clickOptions = False
            self.clickPlayer = True
            self.clickTeam = True
            self.block2clicked = False
            self.block3clicked = False
            self.block4clicked = False
            self.qbClicked = False
            self.rbClicked = False
            self.wrClicked = False
            self.teClicked = False
            self.onPlayer = False
            self.onTeam = False
            self.clickPlayer = False
            self.clickTeam = False
        # 1450, 350, 1650, 400
        elif (1450 <= event.x <= 1650) and (350 <= event.y <= 400) and self.clickStart == True:
            self.showJason()
        elif (1450 <= event.x <= 1650) and (450 <= event.y <= 500) and self.clickStart == True:
            self.showAndy()
        elif (1450 <= event.x <= 1650) and (550 <= event.y <= 600) and self.clickStart == True:
            self.showMike()
        elif (1450 <= event.x <= 1650) and (650 <= event.y <= 700) and self.clickStart == True:
            self.showPat()

    def doPlayer(self):
        while True:
            name1 = self.getUserInput('Enter First Player')
            if name1 == None:
                self.showMessage('Try Again')
                continue
            elif name1 != None:
                first1, last1 = self.splitName(name1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break
        while True:
            name2 = self.getUserInput('Enter Second Player')
            if name2 == None:
                self.showMessage('Try Again')
                continue
            elif name2 != None:
                first2, last2 = self.splitName(name2)
                if self.nameIsValid(first2, last2) == False:
                    self.showMessage('Not A Player!')
                    continue
                elif self.nameIsValid(first2, last2) == True:
                    break

        url = self.getUrl(name2, name1)
        n1, n2, n3, n4 = self.getNames(name2, name1)
        n5 = self.options
        self.accuracies.append(self.Jason.calcWeights(self.position))
        self.accuracies.append(self.Andy.calcWeights(self.position))
        self.accuracies.append(self.Mike.calcWeights(self.position))
        self.accuracies.append(self.Justin.calcWeights(self.position))
        self.accuracies.append(self.Pat.calcWeights(self.position))

        if self.Jason.getWeeklyPick(n1, n2, n3, n4, n5) != None:
            self.Jason.pickWho(n1, n2, n3, n4, 
                self.Jason.getWeeklyPick(n1, n2, n3, n4, n5), n5)
            self.binaries.append(self.Jason.getBinary())

        if self.Andy.getWeeklyPick(n1, n2, n3, n4, n5) != None:
            self.Andy.pickWho(n1, n2, n3, n4, 
                self.Andy.getWeeklyPick(n1, n2, n3, n4, n5), n5)
            self.binaries.append(self.Andy.getBinary())

        if self.Mike.getWeeklyPick(n1, n2, n3, n4, n5) != None:
            self.Mike.pickWho(n1, n2, n3, n4, 
                self.Mike.getWeeklyPick(n1, n2, n3, n4, n5), n5)
            self.binaries.append(self.Mike.getBinary())

        if self.Tags.getWeeklyPick(n1, n2, n3, n4, n5) != None:
            self.Tags.pickWho(n1, n2, n3, n4, 
                self.Tags.getWeeklyPick(n1, n2, n3, n4, n5), n5)
            self.binaries.append(self.Tags.getBinary())

        if self.Pat.getWeeklyPick(n1, n2, n3, n4, n5) != None:
            self.Pat.pickWho(n1, n2, n3, n4, 
                self.Pat.getWeeklyPick(n1, n2, n3, n4, n5), n5)
            self.binaries.append(self.Pat.getBinary())

        x, y = self.linreg(self.accuracies, self.binaries)
        self.firstnamelist = self.Jason.pickWho(n1, n2, n3, n4, 
                            self.Jason.getWeeklyPick(n1, n2, n3, n4, n5), n5)[0][0].split(" ")
        self.firstname = self.firstnamelist[0][0:1].upper() + self.firstnamelist[0][1:] + " " + \
                                self.firstnamelist[1][0:1].upper() + self.firstnamelist[1][1:]
        self.secnamelist = self.Jason.pickWho(n1, n2, n3, n4, 
                            self.Jason.getWeeklyPick(n1, n2, n3, n4, n5), n5)[1][0].split(" ")
        self.secname = self.secnamelist[0][0:1].upper() + self.secnamelist[0][1:] + " " + \
                            self.secnamelist[1][0:1].upper() + self.secnamelist[1][1:]
        x *= 100
        y *= 100
        self.firper = '%.2f' % x
        self.secper = '%.2f' % y
        self.first1 = self.firstnamelist[0]
        self.last1 = self.firstnamelist[1]
        self.first2 = self.secnamelist[0]
        self.last2 = self.secnamelist[1]
        self.imagefirst = self.loadImage(self.getImage(self.first1, self.last1))
        self.imagesecond = self.loadImage(self.getImage(self.first2, self.last2))

    def doTeam(self):
        self.tablepercents = []
        self.tempteam1 = []
        self.tempteam2 = []
        while True:
            qbteam1 = self.getUserInput('Team 1 - QB:')
            if qbteam1 == None:
                self.showMessage('Try Again')
                continue
            elif qbteam1 != None:
                first1, last1 = self.splitName(qbteam1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break
        
        while True:
            rb1team1 = self.getUserInput('Team 1 - RB1:')
            if rb1team1 == None:
                self.showMessage('Try Again')
                continue
            elif rb1team1 != None:
                first1, last1 = self.splitName(rb1team1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break

        while True:
            rb2team1 = self.getUserInput('Team 1 - RB2:')
            if rb2team1 == None:
                self.showMessage('Try Again')
                continue
            elif rb2team1 != None:
                first1, last1 = self.splitName(rb2team1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break            
        
        while True:
            wr1team1 = self.getUserInput('Team 1 - WR1:')
            if wr1team1 == None:
                self.showMessage('Try Again')
                continue
            elif wr1team1 != None:
                first1, last1 = self.splitName(wr1team1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 
        
        while True:
            wr2team1 = self.getUserInput('Team 1 - WR2:')
            if wr2team1 == None:
                self.showMessage('Try Again')
                continue
            elif wr2team1 != None:
                first1, last1 = self.splitName(wr2team1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 
        
        while True:
            teteam1 = self.getUserInput('Team 1 - TE:')
            if teteam1 == None:
                self.showMessage('Try Again')
                continue
            elif teteam1 != None:
                first1, last1 = self.splitName(teteam1)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 

        self.tempteam1 = [qbteam1, rb1team1, rb2team1, wr1team1, wr2team1, teteam1]
        self.team1 = self.tempteam1

        while True:
            qbteam2 = self.getUserInput('Team 2 - QB:')
            if qbteam2 == None:
                self.showMessage('Try Again')
                continue
            elif qbteam2 != None:
                first1, last1 = self.splitName(qbteam2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break
        
        while True:
            rb1team2 = self.getUserInput('Team 2 - RB1:')
            if rb1team2 == None:
                self.showMessage('Try Again')
                continue
            elif rb1team2 != None:
                first1, last1 = self.splitName(rb1team2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break

        while True:
            rb2team2 = self.getUserInput('Team 2 - RB2:')
            if rb2team2 == None:
                self.showMessage('Try Again')
                continue
            elif rb2team2 != None:
                first1, last1 = self.splitName(rb2team2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break            
        
        while True:
            wr1team2 = self.getUserInput('Team 2 - WR1:')
            if wr1team2 == None:
                self.showMessage('Try Again')
                continue
            elif wr1team2 != None:
                first1, last1 = self.splitName(wr1team2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 
        
        while True:
            wr2team2 = self.getUserInput('Team 2 - WR2:')
            if wr2team2 == None:
                self.showMessage('Try Again')
                continue
            elif wr2team2 != None:
                first1, last1 = self.splitName(wr2team2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 
        
        while True:
            teteam2 = self.getUserInput('Team 2 - TE:')
            if teteam2 == None:
                self.showMessage('Try Again')
                continue
            elif teteam2 != None:
                first1, last1 = self.splitName(teteam2)
                if self.nameIsValid(first1, last1) == False:
                    self.showMessage('Not A Player!')
                    continue
                if self.nameIsValid(first1, last1) == True:
                    break 

        self.tempteam2 = [qbteam2, rb1team2, rb2team2, wr1team2, wr2team2, teteam2]
        self.team2 = self.tempteam2
        teamresults = []
        teamN5 = self.options
        for i in range(len(self.team1)):
            self.accuracies = []
            self.binaries = []
            teamurl = self.getUrl(self.team1[i], self.team2[i])
            teamN1, teamN2, teamN3, teamN4 = self.getNames(self.team1[i], self.team2[i])
            if i == 0:
                self.options = 0
            elif i == 1 or i == 2:
                self.options = 1
            elif i == 3 or i == 4:
                self.options = 2
            elif i == 5:
                self.options = 3
            self.accuracies.append(self.Justin.calcWeights(self.position))
            self.accuracies.append(self.Jason.calcWeights(self.position))
            self.accuracies.append(self.Andy.calcWeights(self.position))
            self.accuracies.append(self.Mike.calcWeights(self.position))
            self.accuracies.append(self.Pat.calcWeights(self.position))
            if self.Jason.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5) != None:
                self.Jason.pickWho(teamN1, teamN2, teamN3, teamN4, 
                    self.Jason.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)
                self.binaries.append(self.Jason.getBinary())
            
            if self.Andy.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5) != None:
                self.Andy.pickWho(teamN1, teamN2, teamN3, teamN4, 
                    self.Andy.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)
                self.binaries.append(self.Andy.getBinary())

            if self.Mike.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5) != None:
                self.Mike.pickWho(teamN1, teamN2, teamN3, teamN4, 
                    self.Mike.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)
                self.binaries.append(self.Mike.getBinary())

            if self.Tags.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5) != None:
                self.Tags.pickWho(teamN1, teamN2, teamN3, teamN4, 
                    self.Tags.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)
                self.binaries.append(self.Tags.getBinary())

            if self.Pat.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5) != None:
                self.Pat.pickWho(teamN1, teamN2, teamN3, teamN4, 
                    self.Pat.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)
                self.binaries.append(self.Pat.getBinary())

            x, y = self.linreg(self.accuracies, self.binaries)
            firstnamelist = self.Jason.pickWho(teamN1, teamN2, teamN3, teamN4, 
                            self.Jason.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)[0][0].split(" ")
            firstname = firstnamelist[0][0:1].upper() + firstnamelist[0][1:] + " " + \
                                firstnamelist[1][0:1].upper() + firstnamelist[1][1:]
            secnamelist = self.Jason.pickWho(teamN1, teamN2, teamN3, teamN4, 
                            self.Jason.getWeeklyPick(teamN1, teamN2, teamN3, teamN4, teamN5), teamN5)[1][0].split(" ")
            secname = secnamelist[0][0:1].upper() + secnamelist[0][1:] + " " + \
                            secnamelist[1][0:1].upper() + secnamelist[1][1:]
            if firstname in self.tempteam1:
                teamresults.append(1)
                x *= 100
                xlist = '%.2f' % x
                self.tablepercents.append(xlist)
            elif firstname in self.tempteam2:
                teamresults.append(0)
                y *= 100
                ylist = '%.2f' % y
                self.tablepercents.append(ylist)
        x1, y1 = self.linreg(self.teamWeights, teamresults)
        x1 *= 100
        y1 *= 100
        self.teamper = '%.2f' % x1
        self.team2per = '%.2f' % y1

    # Method from https://stackoverflow.com/questions/10600079/python-beautifulsoup-img-tag-parsing
    def getImage(self, first, last):
        url = f'https://www.fantasypros.com/nfl/players/{first}-{last}.php'
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        images = soup.findAll('img')
        for image in images:
            if 'player' in image['src'] and '250' in image['src']:
                return image['src']

    def linreg(self, accuracylist, binarylist):
        denom = sum(accuracylist)
        numer = 0  
        for index in range(len(binarylist)):
            numer += (accuracylist[index] * binarylist[index])
        frac = numer/denom
        return (frac, 1-frac)

    def getPrelim(self, url, name1, name2):
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        names = soup.find_all('strong')
        final = []
        for name in names:
            if (name.string not in final) and (name.string == name1 or name.string == name2):
                final.append(name.string)
        firstpercent = soup.find("span", attrs={'class':'more'})
        secondpercent = soup.find("span", attrs={'class':'same'})
        return final, firstpercent.string, secondpercent.string

    def drawFeature(self, canvas):
        canvas.create_rectangle(self.width/2 - 140, 30, self.width/2 + 140, 125, 
            fill='khaki')
        canvas.create_text(self.width/2, 75, text='NFL Start/Sit Analyzer', 
            fill='blue', font='Arial 25 bold')

    def drawStart(self, canvas):
        if self.onBlock1:
            canvas.create_rectangle(self.width/2-50, self.height/2-30, 
            self.width/2 + 55, self.height/2 + 30, fill='light coral')
        else:
            canvas.create_rectangle(self.width/2-50, self.height/2-30, 
            self.width/2 + 55, self.height/2 + 30, fill=self.colorstart)
        canvas.create_text(self.width/2, self.height/2, text='* Start *', 
        font='Arial 17 bold')

    def drawOptions(self, canvas):
        canvas.create_rectangle(self.width/2 - 175, 30, self.width/2 + 175, 125, 
        fill='purple')
        canvas.create_text(self.width/2, 75, text='Configure League Options', 
        fill='yellow', font='Arial 25 bold')
        firstX = 250
        firstY = 300
        scoreOptions = ['PPR', 'HALF-PPR', 'Standard']
        if self.onBlock2 or self.block2clicked:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='aquamarine')
        else:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='sea green')
        canvas.create_text(firstX, firstY, fill='gold2', 
        text='PPR', font='Arial 25 bold')
        firstY += 250
        if self.onBlock3 or self.block3clicked:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='aquamarine')
        else:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='sea green')
        canvas.create_text(firstX, firstY, fill='gold2', 
        text='HALF-PPR', font='Arial 25 bold')
        firstY += 250
        if self.onBlock4 or self.block4clicked:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='aquamarine')
        else:
            canvas.create_rectangle(firstX-100, firstY - 100, firstX + 100, 
            firstY + 100, fill='sea green')
        canvas.create_text(firstX, firstY, fill='gold2', 
        text='Standard', font='Arial 25 bold')
        firstY += 250        

        canvas.create_oval(175, 75, 325, 175, fill='purple')
        canvas.create_text(250, 125, text='Scoring', 
            fill='yellow', font='Arial 19 bold')
        canvas.create_oval(self.width/2 - 75, 175, self.width/2 + 75, 275, fill='purple')
        canvas.create_text(self.width/2, 225, text='Position', 
            fill='yellow', font='Arial 19 bold')
        canvas.create_oval(self.width/2 - 75, 515, self.width/2 + 75, 615, fill='purple')
        canvas.create_text(self.width/2, 565, text='Mode', 
            fill='yellow', font='Arial 19 bold')
        canvas.create_oval(1475, 200, 1625, 300, fill='purple')
        canvas.create_text(1550, 250, text='Experts', fill='yellow', font='Arial 19 bold')

        expX = 1450
        expY = 350
        # 1450, 350, 1650, 400
        if self.onJason:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='aquamarine')
        else:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='sea green')
        canvas.create_text(expX + 100, expY + 25, fill='gold2', 
            text='Jason Moore', font='Arial 25 bold')
        expY += 100
        if self.onAndy:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='aquamarine')
        else:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='sea green')
        canvas.create_text(expX + 100, expY + 25, fill='gold2', 
            text='Andy Holloway', font='Arial 25 bold')
        expY += 100
        if self.onMike:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='aquamarine')
        else:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='sea green')
        canvas.create_text(expX + 100, expY + 25, fill='gold2', 
            text='Mike Wright', font='Arial 25 bold')
        expY += 100
        if self.onPat:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='aquamarine')
        else:
            canvas.create_rectangle(expX, expY, expX + 200, 
                expY + 50, fill='sea green')
        canvas.create_text(expX + 100, expY + 25, fill='gold2', 
            text='Pat Fitzmaurice', font='Arial 25 bold')
        
        if self.onSubmit:
            canvas.create_rectangle(self.width/2 - 50, self.height - 100, self.width/2 + 50,
                self.height-50, fill='light sky blue')
        else: 
            canvas.create_rectangle(self.width/2 - 50, self.height - 100, self.width/2 + 50,
                self.height-50, fill='blue')
        canvas.create_text(self.width/2, self.height - 75, text='View Advice', fill='white')

        posX = self.width/2 # 960
        posY = 350
        # 500, 325, 700, 375
        if self.onQB or self.qbClicked:
            canvas.create_rectangle(posX-250, posY - 25, posX - 50, 
                posY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(posX-250, posY - 25, posX - 50, 
                posY + 25, fill='sea green')
        canvas.create_text(750, posY, fill='gold2', 
            text='QB', font='Arial 25 bold')
        posY += 100
        # 500, 425, 700, 475
        if self.onRB or self.rbClicked:
            canvas.create_rectangle(posX-250, posY - 25, posX-50, 
                posY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(posX-250, posY - 25, posX-50, 
                posY + 25, fill='sea green')
        canvas.create_text(750, posY, fill='gold2', 
            text='RB', font='Arial 25 bold')
        posX += 250 # 850
        posY -= 100 # 350
        # 750, 325, 950, 375
        if self.onWR or self.wrClicked:
            canvas.create_rectangle(posX-200, posY - 25, posX, 
                posY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(posX-200, posY - 25, posX, 
                posY + 25, fill='sea green')
        canvas.create_text(1050, posY, fill='gold2', 
            text='WR', font='Arial 25 bold')
        posY += 100
        # 750, 425, 950, 475
        if self.onTE or self.teClicked:
            canvas.create_rectangle(posX-200, posY - 25, posX, 
                posY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(posX-200, posY - 25, posX, 
                posY + 25, fill='sea green')
        canvas.create_text(1050, posY, fill='gold2', 
            text='TE', font='Arial 25 bold')

        modeX = self.width / 2 # 960
        modeY = 675
        # 625, 650, 825, 700 : 625, 750, 825, 800
        if self.onPlayer or self.clickPlayer:
            canvas.create_rectangle(modeX-100, modeY - 25, modeX + 100, 
                modeY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(modeX-100, modeY - 25, modeX + 100, 
                modeY + 25, fill='sea green')
        canvas.create_text(modeX, modeY, fill='gold2', 
            text='Player', font='Arial 25 bold')
        modeY += 100
        # 625, 750, 825, 800
        if self.onTeam or self.clickTeam:
            canvas.create_rectangle(modeX-100, modeY - 25, modeX + 100, 
                modeY + 25, fill='aquamarine')
        else:
            canvas.create_rectangle(modeX-100, modeY - 25, modeX + 100, 
                modeY + 25, fill='sea green')
        canvas.create_text(modeX, modeY, fill='gold2', 
            text='Team', font='Arial 25 bold')

    def drawChoice(self, canvas):
        #label1 = tk.Label(root, text=final[0] + ' ' + firstpercent.string + "\t" + final[1] + ' ' + secondpercent.string, font=('helvetica', 30, 'bold'))
        #canvas1.create_window(500, 230, window=label1)
        canvas.create_text(self.width/2, self.height/2,
            text=(self.firstname + "\t\t\t\t\t\t\t\t\t\t" + self.secname + "\n\n" +  self.firper + "%" + "\t\t\t\t\t\t\t\t\t\t\t" + self.secper + "%"), font=('Arial 25 bold'), fill='white')

    def drawTeamChoice(self, canvas):
        #label1 = tk.Label(root, text=final[0] + ' ' + firstpercent.string + "\t" + final[1] + ' ' + secondpercent.string, font=('helvetica', 30, 'bold'))
        #canvas1.create_window(500, 230, window=label1)
        canvas.create_text(self.width/2, 100,
            text=('Team 1' + "\t\t\t\t\t\t\t\t" + 'Team 2' + "\n\n" +  self.teamper + "%" + "\t\t\t\t\t\t\t\t" + self.team2per + "%"), font=('Arial 25 bold'), fill='black')

    def drawScaleInLocation(self, canvas, beginY, endY, percent):
        beginX = 400
        endX = 1300
        step = 9
        display1 = int(round(float(percent)))
        display2 = 100 - display1
        #print(display1, display2)
        while beginX <= 1300:
            if beginX <= ((900 * (display1/100)) + 400):
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='blue', outline='')
            else:
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='orange', outline='')
            beginX += step

    def drawScalePlayer(self, canvas):
        beginX = 100
        endX = 1700
        beginY = self.height/2 - 150
        endY = self.height/2 - 100
        step = 16
        display1 = int(round(float(self.firper)))
        display2 = 100 - display1
        #print(display1, display2)
        while beginX <= 1700:
            if beginX <= ((1600 * (display1/100)) + 100):
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='blue', outline='')
            else:
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='orange', outline='')
            beginX += step

    def drawScaleTeam(self, canvas):
        beginX = 100
        endX = 1700
        beginY = 20
        endY = 40
        step = 16
        display1 = int(round(float(self.teamper)))
        display2 = 100 - display1
        #print(display1, display2)
        while beginX <= 1700:
            if beginX <= ((1600 * (display1/100)) + 100):
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='blue', outline='')
            else:
                canvas.create_rectangle(beginX, beginY, beginX + step, endY, fill='orange', outline='')
            beginX += step

    def showJason(self):
        self.Jason.getPlot()

    def showAndy(self):
        self.Andy.getPlot()

    def showMike(self):
        self.Mike.getPlot()

    def showPat(self):
        self.Pat.getPlot()

    def nameIsValid(self, first, last):
        url = f'https://www.fantasypros.com/nfl/players/{first}-{last}.php'
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        name = soup.find('h1')
        if name.text == 'NFL Players':
            return False
        else:
            return True

    def drawTeams(self, canvas):
        leftX = 250
        leftY = 300
        rightX = 1450
        rightY = 300
        for name in range(len(self.tempteam1)):
            canvas.create_text(leftX, leftY, text=self.tempteam1[name], fill='blue', font='Arial 23')
            self.drawScaleInLocation(canvas, leftY - 10, leftY + 10, self.tablepercents[name])
            leftY += 100
        for name2 in self.tempteam2:
            canvas.create_text(rightX, rightY, text=name2, fill='orange', font='Arial 23')
            rightY += 100

    def drawRedo(self, canvas):
        canvas.create_rectangle(1500, 900, 1800, 1080, fill='purple')
        canvas.create_text(1650, 955, text='Go Again!', font='Arial 17 bold', fill='yellow')

    def redrawAll(self, canvas):
        if self.clickStart == False:
            canvas.create_rectangle(0, 0, 1920, 1080, fill='ivory3')
            canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.image1))
            self.drawFeature(canvas)
            self.drawStart(canvas)
        elif self.clickOptions == False:
            canvas.create_rectangle(0, 0, 1920, 1080, fill='ivory3')
            self.drawOptions(canvas)
        elif self.clickPlayer == False:
            canvas.create_rectangle(0, 0, 1920, 1080, fill='ivory3')
            canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.imageback))
            canvas.create_image(self.width/2 - 600, 175, image=ImageTk.PhotoImage(self.imagefirst))
            canvas.create_image(self.width/2 + 600, 175, image=ImageTk.PhotoImage(self.imagesecond))
            self.drawChoice(canvas)
            self.drawScalePlayer(canvas)
            self.drawRedo(canvas)
        elif self.clickTeam == False:
            canvas.create_rectangle(0, 0, 1920, 1080, fill='ivory3')
            self.drawTeamChoice(canvas)
            self.drawScaleTeam(canvas)
            self.drawRedo(canvas)
            self.drawTeams(canvas)

class Analyst(object):
    def __init__(self, name):
        self.name = name
        self.accuracy = 0.0
        self.result = []
        self.newnames = [None, None]
    def getAccuracy(self):
        #website = requests.get('https://www.fantasypros.com/nfl/accuracy/2009-2015.php')
        #target = SoupStrainer('span',{'class': 'expert-name'})
        #soup = bs4.BeautifulSoup(website, parse_only=target)
        #percentage = soup.find("td", {"style": "text-align:center; vertical-align:middle; \
        #background:#f7f7f7; font-weight:bold;"}).get_text(strip=True)
        return self.accuracy
    def extractWeights(self):
        website1 = requests.get('https://www.fantasypros.com/nfl/accuracy/')
        soup = bs4.BeautifulSoup(website1.text, 'html.parser')
        tbl = soup.find('table')
        for row in tbl.find_all('tr')[1:]:
            res = row.text
            #.replace('\n\n', '  ').strip()
            res_list = res.split()
            if self.name in res:
                tds = row.find_all('td', attrs={'class': 'center'})
                arr1 = tds[1].text + ' ' + tds[2].text + ' ' + \
                tds[3].text + ' ' + tds[4].text + ' ' + tds[5].text + ' ' + tds[6].text
                self.result.append(arr1)
        website2 = requests.get('https://www.fantasypros.com/nfl/accuracy/?year=2019')
        soup = bs4.BeautifulSoup(website2.text, 'html.parser')
        tbl2 = soup.find('table')
        for row2 in tbl2.find_all('tr')[1:]:
            res2 = row2.text.replace('\n\n', '  ').strip()
            res2_list = res2.split()
            if self.name in res2:
                tds2 = row2.find_all('td', attrs={'class': 'center'})
                arr2 = tds2[1].text + ' ' + tds2[2].text + ' ' + \
                tds2[3].text + ' ' + tds2[4].text + ' ' + tds2[5].text + ' ' + tds2[6].text
                self.result.append(arr2)
        website3 = requests.get('https://www.fantasypros.com/nfl/accuracy/?year=2018')
        soup = bs4.BeautifulSoup(website3.text, 'html.parser')
        tbl3 = soup.find('table')
        for row3 in tbl3.find_all('tr')[1:]:
            res3 = row3.text.replace('\n\n', '  ').strip()
            res3_list = res3.split()
            if self.name in res3:
                tds3 = row3.find_all('td', attrs={'class': 'center'})
                arr3 = tds3[1].text + ' ' + tds3[2].text + ' ' + \
                tds3[3].text + ' ' + tds3[4].text + ' ' + tds3[5].text + ' ' + tds3[6].text
                self.result.append(arr3)
        website4 = requests.get('https://www.fantasypros.com/nfl/accuracy/?year=2017')
        soup = bs4.BeautifulSoup(website4.text, 'html.parser')
        tbl4 = soup.find('table')
        for row4 in tbl4.find_all('tr')[1:]:
            res4 = row4.text.replace('\n\n', '  ').strip()
            res4_list = res4.split()
            if self.name in res4:
                tds4 = row4.find_all('td', attrs={'class': 'center'})
                arr4 = tds4[1].text + ' ' + tds4[2].text + ' ' + \
                tds4[3].text + ' ' + tds4[4].text + ' ' + tds4[5].text + ' ' + tds4[6].text
                self.result.append(arr4)
        website5 = requests.get('https://www.fantasypros.com/nfl/accuracy/?year=2016')
        soup = bs4.BeautifulSoup(website5.text, 'html.parser')
        tbl5 = soup.find('table')
        for row5 in tbl5.find_all('tr')[1:]:
            res5 = row5.text.replace('\n\n', '  ').strip()
            res5_list = res5.split()
            if self.name in res5:
                tds5 = row5.find_all('td', attrs={'class': 'center'})
                arr5 = tds5[1].text + ' ' + tds5[2].text + ' ' + \
                tds5[3].text + ' ' + tds5[4].text + ' ' + tds5[5].text + ' ' + tds5[6].text
                self.result.append(arr5)
        return self.result
    @staticmethod
    def createScale(average):
        weight = 0.95
        n = 0
        while n <= 130:
            if n <= average < n + 5:
                return weight
            else:
                n += 5
                weight -= 0.05
    @staticmethod
    def calcAverage(L):
        total = 0
        numbers = 0
        for item in L:
            if isinstance(item, int):
                numbers += 1
                total += item
        return total / numbers

    def calcWeights(self, position):
        currWeight = 0
        #numberOfAverage = 5
        self.rankings = []
        for index in range(len(self.result)):
            newlist = self.result[index].split()
            for item in range(len(newlist)):
                if newlist[item] != '-':
                    newlist[item] = int(float(newlist[item]))
            #print(newlist)
            self.rankings.append(newlist[position])
        #print(rankings)
        avg = Analyst.calcAverage(self.rankings)
        self.accuracy = Analyst.createScale(avg)
        #self.accuracy = currWeight / numberOfAverage
        return self.accuracy

    def getYList(self, position):
        rankings = []
        for index in range(len(self.result)):
            newlist = self.result[index].split()
            for item in range(len(newlist)):
                if newlist[item] != '-':
                    newlist[item] = int(float(newlist[item]))
            #print(newlist)
            rankings.append(newlist[position])
        #print(rankings)
        #self.accuracy = currWeight / numberOfAverage
        return rankings

    def getWeeklyPick(self, first1, last1, first2, last2, scoring):
        choice = []
        url = f'https://www.fantasypros.com/nfl/start/{first1}-{last1}-{first2}-{last2}.php?scoring={scoring}'
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        tbl = soup.find('table')
        for row in tbl.find_all('tr'):
            res = row.text
            if self.name in res:
                tds = row.find_all('td', attrs={'class': 'center data'})
                raw1 = tds[-3].text.replace('#', '', 1)
                raw2 = tds[-2].text.replace('#', '', 1)
                choice.append(raw1)
                choice.append(raw2)
                return choice

    def pickWho(self, first1, last1, first2, last2, L, scoring):
        names = []
        url = f'https://www.fantasypros.com/nfl/start/{first1}-{last1}-{first2}-{last2}.php?scoring={scoring}'
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        tbl = soup.find('table') 
        row = tbl.find_all('tr')[1]
        res = row.text
        res_list = res.split()
        for name in range(len(res_list)):
            res_list[name] = res_list[name].lower()
            # method used from https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
            res_list[name] = res_list[name].translate(str.maketrans('', '', string.punctuation))
        for name2 in range(len(res_list)):
            if (res_list[name2] not in names and (res_list[name2] == first1 or res_list[name2] == first2 or
            res_list[name2] == last1 or res_list[name2] == last2)):
                names.append(res_list[name2])
        self.newnames[0] = [' '.join((names[0], names[1]))]
        self.newnames[1] = [' '.join((names[2], names[3]))]
        self.newnames[0].append(L[0]) 
        self.newnames[1].append(L[1])
        return self.newnames

    def getBinary(self):
        if int(self.newnames[0][1]) >= int(self.newnames[1][1]):
            return 0
        else:
            return 1
    # self.Jason.getPlot(self.Jason.getYList(0))
    # General model used from https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html
    def getPlot(self):
        fig, axs = plt.subplots(2,2)
        x = [2016, 2017, 2018, 2019, 2020]
        y = self.getYList(0)
        axs[0, 0].plot(x, y)
        axs[0, 0].set_title('QB Accuracy')
        y = self.getYList(1)
        axs[0, 1].plot(x, y, 'tab:orange')
        axs[0, 1].set_title('RB Accuracy')
        y = self.getYList(2)
        axs[1, 0].plot(x, y, 'tab:green')
        axs[1, 0].set_title('WR Accuracy')
        y = self.getYList(3)
        axs[1, 1].plot(x, y, 'tab:red')
        axs[1, 1].set_title('TE Accuracy')

        for ax in axs.flat:
            ax.set(xlabel='Year', ylabel='Expert Accuracy Ranking')

        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        plt.show()

    def getRBs(self, scoring):
        rbs = []
        scoring = scoring.lower()
        if scoring == 'ppr':
            url = 'https://www.fantasypros.com/nfl/rankings/ppr-rb.php'
        elif scoring == 'half':
            url = 'https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb.php'
        elif scoring == 'std':
            url = 'https://www.fantasypros.com/nfl/rankings/rb.php'
        website = requests.get(url)
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        tbl = soup.find('table') 
        row = tbl.find_all('tr')[1]
        res = row.text
        res_list = res.split()
        return res_list
    
MyApp(width=1920, height=1080)
