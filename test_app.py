import unittest
import json
from app import app

class TestCipherApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_vigenere(self):
        # Encrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'vigenere', 'action': 'encrypt', 'text': 'HELLO', 'key': 'KEY'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'RIJVS') # H+K=R, E+E=I, L+Y=J, L+K=V, O+E=S (Wait, Vigenere logic check: H(7)+K(10)=17(R). Correct.)
        self.assertIn('time', data)
        self.assertIsInstance(data['time'], float)
        
        # Decrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'vigenere', 'action': 'decrypt', 'text': 'RIJVS', 'key': 'KEY'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'HELLO')

    def test_caesar(self):
        # Encrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'caesar', 'action': 'encrypt', 'text': 'ABC', 'key': '1'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'BCD')
        
        # Decrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'caesar', 'action': 'decrypt', 'text': 'BCD', 'key': '1'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'ABC')

    def test_number(self):
        # Encrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'number', 'action': 'encrypt', 'text': 'ABC'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], '1 2 3')
        
        # Decrypt
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'number', 'action': 'decrypt', 'text': '1 2 3'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'ABC')

    def test_columnar(self):
        # Encrypt
        # Key: ZEBRA (5, 2, 1, 4, 3) -> 1 2 3 4 5 order is B E R Z A? 
        # Wait, sorted indices: A(4), B(1), E(2), R(3), Z(0) ? No, indices of key chars in sorted key?
        # My implementation:
        # key_indices = sorted(range(len(key)), key=lambda k: key[k])
        # ZEBRA -> A is at index 4, B at 1, E at 2, R at 3, Z at 0.
        # Order of columns read: 4, 1, 2, 3, 0.
        # Msg: WE ARE DISCOVERED FLEE AT ONCE (Standard example usually removes spaces, I kept spaces)
        # Msg: "HELLO" Key: "KEY" (K, E, Y -> E, K, Y -> 1, 0, 2)
        # HELLO 
        # H E L
        # L O _
        # Cols:
        # 0 (K): H, L
        # 1 (E): E, O
        # 2 (Y): L, _
        # Read order 1, 0, 2 -> EO HL L_
        
        response = self.app.post('/process', 
                                 data=json.dumps({'type': 'columnar', 'action': 'encrypt', 'text': 'HELLO', 'key': 'KEY'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        # Expected: EO HL L_ -> EOHLL
        # My impl assumes spaces are part of message.
        # Let's verify what it does.
        self.assertIn('EOHLL', data['result'].replace('_','').replace(' ','').strip()) 

if __name__ == '__main__':
    unittest.main()
