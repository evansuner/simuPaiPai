const express = require('express');
const Crypto = require('crypto-js');
const BodyParser = require('body-parser');
// const Buffer = require('buffer');
const app = express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  res.send('Hello, Welcome to PaiPai Decryptor.');
});

app.post('/decryptor', (req, res) => {
  const data = req.body.data;
  const key = req.body.key;
  const response = decryptor(data, key);
  res.send(response);
});

function decryptor(d, k) {
  const decrypted_data = atob(d)
  const ms = Crypto.MD5(k).toString();
  const kk = Crypto.enc.Utf8.parse(ms)
  const kv = Crypto.enc.Utf8.parse(ms.slice(16, 32))
  const decrypted = Crypto.AES.decrypt(decrypted_data, kk, { iv: kv, padding: Crypto.pad.Pkcs7, mode: Crypto.mode.CBC })
  let data = decrypted.toString(Crypto.enc.Utf8)
  return JSON.parse(data);
}



const server = app.listen(7799, '0.0.0.0', () => {
  const address = server.address();
  console.log(`Server listening on http://${ address.address }:${ address.port }`);
});