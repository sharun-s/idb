titles='Air Vice Mar. |Br. |Dr. (Kum.) |Dr. (Mrs.) |Dr. (Ms.) |Dr. (Smt.) |(Dr.) |Dr. |Isai |Kumari |Kum. |Late Shri |Late Smt. |Late (Smt) |Maj. Gen. |Maj. |Miss |Ms. |Ms |Nartaki |Prof. |Prof.(Dr) |Prof. (Dr.) |Prof |Sadhguru |Sheik |Shri |Vice Adm. |Adm. |(Miss) |(Smt.) |Smt. '

initial=lambda n: ' '.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]
tightinitial=lambda n: ''.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]

#name - dProps['label']
initlabels=lambda name:{initial(i):i for i in name }
tinitlabels=lambda name:{tightinitial(i):i for i in name }