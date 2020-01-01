class PhoneTokenizer(object):
  def __init__(self):
    self.phone_to_idx = dict()
    self.idx_to_phone = dict()
    self.dict_size = 0

  def build_phone_dict(self, phoneme_file):
    with open(phoneme_file, 'r', encoding='utf-8') as f:
      for idx, line in enumerate( f.readlines() ):
        phone = line.strip().split()[0]
        self.phone_to_idx[ phone ] = idx + 1
        self.idx_to_phone[ idx+1 ] = phone
      self.dict_size = len(self.phone_to_idx)

  def text_to_seqs(self, sent_arr):
    idx_seqs = []
    for sent in sent_arr:
      if isinstance(sent, str):
        sent = sent.split()
      sent_to_idx = []
      for phone in sent:
        sent_to_idx.append( self.phone_to_idx[phone] )
      idx_seqs.append( sent_to_idx )
      
    return idx_seqs

  def seqs_to_text(self, seq_arr):
    phone_sents = []

    for seq in seq_arr:
      phones = []

      for idx in seq:
        ph = self.idx_to_phone[idx] if idx in self.idx_to_phone else None
        if ph is not None:
          phones.append( ph )
          
      phone_sents.append( ' '.join(phones) )

    return phone_sents