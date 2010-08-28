honorifics = frozenset(map(str.strip, """
Doctor Dr Dr.
Mr Mr.
Miss Ms Ms.
Mrs Mrs.
Captain Capt. Capt
Professor Prof Prof.
Reverend Rev Rev.
Senator Sen Sen.
""".split()))

honorifics_all = """
#A.
Adj.
Adm.
Adv.
Asst.
#B.
Bart.
Bldg.
Brig.
Bros.
C.
Capt.
Cmdr.
Col.
Comdr.
Con.
Cpl.
D.
DR.
Dr.
E.
Ens.
F.
G.
Gen.
Gov.
H.
Hon.
Hosp.
I.
Insp.
J.
K.
L.
Lt.
M.
M.
MM.
MR.
MRS.
MS.
Maj.
Messrs.
Mlle.
Mme.
Mr.
Mrs.
Ms.
Msgr.
N.
O.
Op.
Ord.
P.
Pfc.
Ph.
Prof.
Pvt.
Q.
R.
Rep.
Reps.
Res.
Rev.
Rt.
S.
Sen.
Sens.
Sfc.
Sgt.
Sr.
St.
Supt.
Surg.
T.
U.
V.
W.
X.
Y.
Z.
v.
vs.
"""
