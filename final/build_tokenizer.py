import os, sys, pickle
from phone_tokenizer import PhoneTokenizer

PHONE_LIST_FILEPATH = sys.argv[1]
TOKENIZER_SAVE_PATH = sys.argv[2]

phone_tokenizer = PhoneTokenizer()
phone_tokenizer.build_phone_dict( PHONE_LIST_FILEPATH )
print (phone_tokenizer.phone_to_idx)
pickle.dump(phone_tokenizer, open(TOKENIZER_SAVE_PATH, 'wb'))