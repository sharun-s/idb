titles='Air Vice Mar. |Br. |Dr. Rm. |Dr.\(Kum.\) |Dr. \(Kum.\) |Dr.\(Ms.\) |Dr.\(Mrs.\) |Dr. \(Mrs.\) |Dr. \(Ms.\) |Dr. \(Smt.\) |\(Dr.\) |Dr. |Dr.|Isai |Kumari |Kum. |Late Shri |Late Smt. |Late \(Smt\) |Maj. Gen. |Maj. |Gen. |Miss |Ms. |Ms |Nartaki |Prof.\(Dr\) |Prof. \(Dr.\) |Prof. |Prof |Sadhguru |Sheik |Shri |Vice Adm. |Adm. |\(Miss\) |\(Smt.\) |Smt. '

initial=lambda n: ' '.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]
tightinitial=lambda n: ''.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]

#name - dProps['label']
initlabels=lambda namelist:{initial(i):i for i in namelist }
tinitlabels=lambda namelist:{tightinitial(i):i for i in namelist }