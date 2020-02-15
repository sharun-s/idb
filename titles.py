# usualful when stripping title from name
titles='Swami |Sardar |Sheik |Father |Fr. |Most Venerable |Her Royal Highness Princess |Hon. Commodore |Bishop |Nawab |Rear Admiral |Admiral |Prof\.\(Mrs\.\) |His Holiness |Congressman |Sir |Card. |Maulana |Air Com\. |Wing Cdr |Lt\.Gen\.\(Rt\.\) |Late\. \(Gen\.\) |His Excellency |Acharya |Vaidya |Vaidyan |Yogacharya |Muni |Lord |Maharaj |Kumar |Rajmata |Rajkumari |Rani |Hakim |Sant |Guru |Air Marshal |Air Mar\. |Air Vice Marshal |Air Vice Mar\. |Ar\.V\.Mar\. |Br\. |Dr\. Rm\. |Dr\.\(Kum.\) |Dr\. \(Kum.\) |Dr\.\(Ms.\) |Dr\.\(Mrs.\) |Dr\. \(Mrs\.\) |Dr\. \(Ms.\) |Dr\. \(Smt.\) |\(Dr\.\) |Dr\. |Dr\.|Isai |Kumari |Kum\. |Late Shri |Late Smt\. |Late \(Shri\) |Late \(Smt\) |Late |Major |Maj\. Gen\. |Maj\. |Lt\. |Gen\. |Nartaki |Prof\.\(Dr\) |Prof\. \(Dr.\) |Prof\. |Prof |Sadhguru |Sheik |Shri |Vice Adm\. |Adm\. |\(Miss\) |\(Smt\.\) |Smt\. |Smt |Mrs\. |Grp\.Capt\. |Hon\. Capt\. |Capt\. |Ustad |Begum |Begam |Sister |Rev\. |Rev |Pandit |Pandita |Pt\. |Justice |Mr\. |Col\. |Brig\.\(Retd\) |Brig\. |Late\. \(Gen\.\) Miss |Ms\. |Ms '

#5-106 titles found
#group them
#figure out the order ^(?=.*Prof)(?=.*Smt)
#optional prefix = (
#optional suffix = ).

# prefix='\('
# suffix='[\.\)]'
# lookahead=lambda x:"(?=.*{0})".format(x)
# prefix_suffix_lookahead=lambda x:"(?=.*{1}?{0}{2}?)".format(x,prefix,suffix)
# acad=["Prof","Dr","Smt","Mrs","Miss","Ms"]
# def genlookaheadregex(tokenlist):
# 	r=''
# 	for i in tokenlist:
# 		r=r+lookahead(i)
# 	return r

# title honorific salutation

mil='''
Hon. Commodore |
Rear Admiral |
Admiral |
Air Com\. |
Wing Cdr |
Lt\.Gen\.\(Rt\.\) |
Late\. \(Gen\.\) |
Air Marshal |
Air Mar\. |
Air Vice Marshal |
Air Vice Mar\. |
Ar\.V\.Mar\. |
Br\. |
Major |
Maj\. Gen\. |
Maj\. |
Lt\. |
Gen\. |
Vice Adm\. |
Adm\. |
Grp\.Capt\. |
Hon\. Capt\. |
Capt\. |
Col\. |
Brig\.\(Retd\) |
Brig\. |
Late\. \(Gen\.\) |
'''

groupedtitles='''
Swami |
Acharya |
Vaidya |
Vaidyan |
Yogacharya |
Muni |
Sant |
Guru |
Sadhguru |
Pandit |
Pandita |
Pt\. |

His Holiness |
Most Venerable |

Justice |

Sheik |
Maulana |
Hakim |
Ustad |
Begum |
Begam |

Sister |
Rev\. |
Rev |
Father |
Fr. |
Card. |
Bishop |

Her Royal Highness Princess |
Sardar |
Nawab |
Congressman |
His Excellency |
Lord |
Lady |
Sir |
Maharaj |
Kumar |
Rajmata |
Rajkumari |
Rani |

Prof\.\(Mrs\.\) |
Dr\. Rm\. |
Dr\.\(Kum.\) |
Dr\. \(Kum.\) |
Dr\.\(Ms.\) |
Dr\.\(Mrs.\) |
Dr\. \(Mrs\.\) |
Dr\. \(Ms.\) |
Dr\. \(Smt.\) |
\(Dr\.\) |
Dr\. |
Dr\.|
Prof\.\(Dr\) |
Prof\. \(Dr.\) |
Prof\. |
Prof |

Isai |
Nartaki |

Kumari |
Kum\. |
Late Shri |
Late Smt\. |
Late \(Shri\) |
Late \(Smt\) |
Late |
Shri |
\(Miss\) |
\(Smt\.\) |
Smt\. |
Smt |
Mrs\. |
Mr\. |
Miss |
Ms\. |
Ms '''


# this adds () around each group in ops where its reqd to work out which title name has
gtitles="|".join("({0})".format(i) for i in titles.split('|'))

initial=lambda n: ' '.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]
tightinitial=lambda n: ''.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]

#name - dProps['label']
initlabels=lambda namelist:{initial(i):i for i in namelist }
tinitlabels=lambda namelist:{tightinitial(i):i for i in namelist }