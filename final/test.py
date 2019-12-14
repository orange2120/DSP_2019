import sys, pickle

# seq = "l v4 sh ix4 ii iang2 ch un1 ii ian1 j ing3 d a4 k uai4 uu un2 zh ang1 d e5 d i3 s e4 s iy4 vv ve4 d e5 l in2 l uan2 g eng4 sh ix4 l v4 d e5 x ian1 h uo2 x iu4 m ei4 sh ix1 ii i4 aa ang4 r an2"
seq = "ii iu3 ii i4 j ia1 g e4 t i3 zh ix4 p in2 ch ang3 b en3 g ai1 ii iong4 uu uan2 zh eng3 d e5 x ing2 c ai2 sh eng1 ch an3 m en2 ch uang1 q ve4 ii iong4 b an4 j ie2 c ai2 d a3 j ie2 c ou4 h e5"
sl = []
sl.append(seq)

with open('./pickle/phone_tokenizer.pkl', 'rb') as f:
    ptk = pickle.load(f)

out = ptk.text_to_seqs(sl)

print(out)
