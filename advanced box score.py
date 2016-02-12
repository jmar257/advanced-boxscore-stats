# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 18:54:35 2016

@author: John
"""

import pandas
from time import strptime

opp = 'Georgia'
try:
    boxscore = pandas.read_csv(opp + ".csv", header = 0)
except:
    boxscore = pandas.read_csv(opp + ".csv", header = 1)

l_fg = []
fg_att = []
fg_made_mon = []
fg_made = []

for line in boxscore['FG']:
    s = str(line)
    if s[-1]  in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        try:
            int(s[-1])
            s = s[::-1]
        except:
            pass
    l_fg.append(s.split('-'))

fg_att, fg_made_mon = zip(*l_fg)

for mon in fg_made_mon:
    try:
        fg_made.append(strptime(mon,'%b').tm_mon)
    except:
        fg_made.append(float(mon))

boxscore.insert(3, 'FG_Made', fg_made)
boxscore.insert(4, 'FG_Att', fg_att)
boxscore.drop('FG', inplace=True, axis=1)

l_threes = []
threes_att = []
threes_made_mon = []
threes_made = []

for line in boxscore['3FG']:
    s = str(line)
    if s[-1]  in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        try:
            int(s[-1])
            s = s[::-1]
        except:
            pass
    l_threes.append(s.split('-'))

threes_att, threes_made_mon = zip(*l_threes)

for mon in threes_made_mon:
    try:
        threes_made.append(strptime(mon,'%b').tm_mon)
    except:
        threes_made.append(float(mon))

boxscore.insert(5, '3PT_Made', threes_made)
boxscore.insert(6, '3PT_Att', threes_att)
boxscore.drop('3FG', inplace=True, axis=1)

l_ft = []
ft_att = []
ft_made_mon = []
ft_made = []

for line in boxscore['FT']:
    s = str(line)
    if s[-1]  in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        try:
            int(s[-1])
            s = s[::-1]
        except:
            pass
    l_ft.append(s.split('-'))

ft_att, ft_made_mon = zip(*l_ft)

for mon in ft_made_mon:
    try:
        ft_made.append(strptime(mon,'%b').tm_mon)
    except:
        ft_made.append(float(mon))

boxscore.insert(7, 'FT_Made', ft_made)
boxscore.insert(8, 'FT_Att', ft_att)
boxscore.drop('FT', inplace=True, axis=1)

boxscore['PTS'] = boxscore['PTS'].astype(float)
boxscore['FG_Made'] = boxscore['FG_Made'].astype(float)
boxscore['FG_Att'] = boxscore['FG_Att'].astype(float)
boxscore['3PT_Made'] = boxscore['3PT_Made'].astype(float)
boxscore['3PT_Att'] = boxscore['3PT_Att'].astype(float)
boxscore['FT_Att'] = boxscore['FT_Att'].astype(float)
boxscore['FT_Made'] = boxscore['FT_Made'].astype(float)
boxscore['OR'] = boxscore['OR'].astype(float)
boxscore['DR'] = boxscore['DR'].astype(float)
boxscore['REB'] = boxscore['REB'].astype(float)
boxscore['A'] = boxscore['A'].astype(float)
boxscore['PF'] = boxscore['PF'].astype(float)
boxscore['TO'] = boxscore['TO'].astype(float)
boxscore['BL'] = boxscore['BL'].astype(float)
boxscore['ST'] = boxscore['ST'].astype(float)
boxscore['MIN'] = boxscore['MIN'].astype(float)
boxscore['+/-'] = boxscore['+/-'].astype(float)

boxscore['PER'] = ((((boxscore['FG_Made'] * 85.910) + (boxscore['ST'] * 53.897) + (boxscore['3PT_Made'] * 51.757) + (boxscore['FT_Made'] * 46.845) + (boxscore['BL'] * 39.190) + (boxscore['OR'] * 39.190) + (boxscore['A'] * 34.677) + (boxscore['DR'] *14.707) - (boxscore['PF'] * 17.174) - ((boxscore['FT_Att']-boxscore['FT_Made']) * 20.091) - ((boxscore['FG_Att']-boxscore['FG_Made']) * 39.190) - (boxscore['TO'] * 53.897))) * (1 / boxscore['MIN']))

#Scale Gamescore by minutes in game, don't scale out of game, otherwise raise error
if sum(boxscore['MIN'])<200:
    boxscore['Gamescore'] = ((boxscore['PTS'] + (.4 * boxscore['FG_Made']) - (.7 * boxscore['FG_Att']) - (.4 * (boxscore['FT_Att'] - boxscore['FT_Made'])) + (.7 * boxscore['OR']) + (.3 * boxscore['DR']) + boxscore['ST'] + (.7 * boxscore['A']) + (.7 * boxscore['BL']) - (.4 * boxscore['PF']) - boxscore['TO']))*(40/boxscore['MIN'])
elif sum(boxscore['MIN'])==200:
    boxscore['Gamescore'] = ((boxscore['PTS'] + (.4 * boxscore['FG_Made']) - (.7 * boxscore['FG_Att']) - (.4 * (boxscore['FT_Att'] - boxscore['FT_Made'])) + (.7 * boxscore['OR']) + (.3 * boxscore['DR']) + boxscore['ST'] + (.7 * boxscore['A']) + (.7 * boxscore['BL']) - (.4 * boxscore['PF']) - boxscore['TO']))
else:
    raise ValueError('Number of minutes is >200')

boxscore['eFG%'] = (boxscore['FG_Made'] + 0.5 * boxscore['3PT_Made']) / boxscore['FG_Att']
boxscore['TOV%'] = boxscore['TO'] / (boxscore['FG_Att'] + 0.44 + boxscore['FT_Att'] + boxscore['TO'])
#boxscore['ORB'] = boxscore['OR'] / (boxscore['OR'] + boxscore['Opp_DR']) #need to incorporate opp's box score to calculate ORB and DRB
#boxscore['DRB'] = boxscore['DR'] / (boxscore['Opp_OR'] + boxscore['DR'])
boxscore['FTF'] = boxscore['FT_Made'] / boxscore['FG_Att']

boxscore['Usage Rate'] = 100 * ((boxscore['FG_Att'] + 0.44 * boxscore['FT_Att'] + boxscore['TO']) * (sum(boxscore['MIN']) / 5)) / (boxscore['MIN'] * (sum(boxscore['FG_Att']) + 0.44 * sum(boxscore['FT_Att']) + sum(boxscore['TO'])))

boxscore = boxscore.sort_values('PER', ascending = False)


header = ['#', 'Player', 'MIN', 'PER', 'Gamescore', 'eFG%', 'TOV%', 'FTF', 'Usage Rate', '+/-']
boxscore.to_csv(opp + ' Gamescore and PER.csv', columns = header, float_format = '%.2f')


file = open(opp + ' Gamescore and PER.csv', 'a')
file.write('\n,*Asterisks denote starters')
file.close()
