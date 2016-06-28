def getfile(file_id, file_key):
  key = base64_to_a32(file_key)
  k = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6], key[3] ^ key[7])
  iv = key[4:6] + (0, 0)
  meta_mac = key[6:8]
 
  file = api_req({'a': 'g', 'g': 1, 'p': file_id})
  dl_url = file['g']
  size = file['s']
  attributes = base64urldecode(file['at']) 
  attributes = dec_attr(attributes, k)
 
  print "Downloading %s (size: %d), url = %s" % (attributes['n'], size, dl_url)
 
  infile = urllib.urlopen(dl_url)
  outfile = open(attributes['n'], 'wb')
  decryptor = AES.new(a32_to_str(k), AES.MODE_CTR, counter = Counter.new(128, initial_value = ((iv[0] 32) + iv[1]) &lt;&lt; 64))
 
  file_mac = [0, 0, 0, 0]
  for chunk_start, chunk_size in sorted(get_chunks(file['s']).items()):
    chunk = infile.read(chunk_size)
    chunk = decryptor.decrypt(chunk)
    outfile.write(chunk)
 
    chunk_mac = [iv[0], iv[1], iv[0], iv[1]]
    for i in xrange(0, len(chunk), 16):
      block = chunk[i:i+16]
      if len(block) % 16:
        block += '\0' * (16 - (len(block) % 16))
      block = str_to_a32(block)
      chunk_mac = [chunk_mac[0] ^ block[0], chunk_mac[1] ^ block[1], chunk_mac[2] ^ block[2], chunk_mac[3] ^ block[3]]
      chunk_mac = aes_cbc_encrypt_a32(chunk_mac, k)
 
    file_mac = [file_mac[0] ^ chunk_mac[0], file_mac[1] ^ chunk_mac[1], file_mac[2] ^ chunk_mac[2], file_mac[3] ^ chunk_mac[3]]
    file_mac = aes_cbc_encrypt_a32(file_mac, k)
 
  outfile.close()
  infile.close()
 
  if (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3]) != meta_mac:
    print "MAC mismatch"
  else:
    print "MAC OK"
getfile('6N0gmRLK', 'VsN9gLdiYbxMVTA-AdsRjsvezMpdEqiR9ngwrS6gR7k')