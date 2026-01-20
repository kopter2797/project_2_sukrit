import time
import re
from flask import Flask, render_template, request, jsonify
from ciphers import Vigenere, Caesar, Number, Columnar

app = Flask(__name__)

# Common English words for scoring
COMMON_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
    'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
    'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
    'hello', 'world', 'test', 'message', 'secret', 'code', 'key', 'text', 'word', 'letter'
}

# Expected English letter frequency (approximate)
ENGLISH_FREQ = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.1, 'z': 0.07
}

def score_text(text):
    """
    Score how likely the text is readable English.
    Higher score = more likely to be correct decryption.
    """
    if not text:
        return 0
    
    score = 0
    text_lower = text.lower()
    
    # 1. Common words matching (weighted heavily)
    words = re.findall(r'[a-z]+', text_lower)
    if words:
        common_count = sum(1 for w in words if w in COMMON_WORDS)
        word_ratio = common_count / len(words)
        score += word_ratio * 50  # Max 50 points
    
    # 2. Letter frequency analysis
    letters_only = re.sub(r'[^a-z]', '', text_lower)
    if len(letters_only) > 0:
        letter_counts = {}
        for char in letters_only:
            letter_counts[char] = letter_counts.get(char, 0) + 1
        
        # Calculate frequency deviation from expected English
        total_deviation = 0
        for letter, expected_freq in ENGLISH_FREQ.items():
            actual_freq = (letter_counts.get(letter, 0) / len(letters_only)) * 100
            total_deviation += abs(expected_freq - actual_freq)
        
        # Lower deviation = higher score (max 30 points)
        freq_score = max(0, 30 - total_deviation / 2)
        score += freq_score
    
    # 3. Readable character ratio (letters, spaces, punctuation)
    readable_chars = sum(1 for c in text if c.isalpha() or c.isspace() or c in '.,!?;:\'"')
    if len(text) > 0:
        readable_ratio = readable_chars / len(text)
        score += readable_ratio * 20  # Max 20 points
    
    return round(score, 2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    start_time = time.time()
    data = request.json
    cipher_type = data.get('type')
    action = data.get('action') # 'encrypt' or 'decrypt'
    text = data.get('text', '')
    key = data.get('key', '')

    print(f"Processing {cipher_type} with key: {key!r}")
    result = "ข้อผิดพลาด: คำขอไม่ถูกต้อง (Error: Unknown Request)"

    if action == 'encrypt':
        if cipher_type == 'vigenere':
            result = Vigenere.encrypt(text, key)
        elif cipher_type == 'caesar':
            result = Caesar.encrypt(text, key)
        elif cipher_type == 'number':
            result = Number.encrypt(text, key)
        elif cipher_type == 'columnar':
            result = Columnar.encrypt(text, key)
    elif action == 'decrypt':
        if cipher_type == 'vigenere':
            result = Vigenere.decrypt(text, key)
        elif cipher_type == 'caesar':
            result = Caesar.decrypt(text, key)
        elif cipher_type == 'number':
            result = Number.decrypt(text, key)
        elif cipher_type == 'columnar':
            result = Columnar.decrypt(text, key)
            
    elif action == 'autocrack':
        # Support multiple separators: newline, comma, space
        import re
        keys = re.split(r'[\n,\s]+', key)
        keys = [k.strip() for k in keys if k.strip()]
        scored_results = []
        
        for k in keys:
            try:
                if cipher_type == 'vigenere':
                    res = Vigenere.decrypt(text, k)
                elif cipher_type == 'caesar':
                    res = Caesar.decrypt(text, k)
                elif cipher_type == 'number':
                    res = Number.decrypt(text, k)
                elif cipher_type == 'columnar':
                    res = Columnar.decrypt(text, k)
                else:
                    res = "Error: Unknown Cipher"
                
                text_score = score_text(res)
                scored_results.append({
                    'key': k,
                    'result': res,
                    'score': text_score
                })
            except Exception as e:
                scored_results.append({
                    'key': k,
                    'result': f"Error ({str(e)})",
                    'score': 0
                })
        
        if not scored_results:
            result = "No valid keys provided."
        else:
            # Sort by score (highest first)
            scored_results.sort(key=lambda x: x['score'], reverse=True)
            
            # Simple output - just key and result
            best = scored_results[0]
            result = f"KEY ตัวจริง: {best['key']}\nผลลัพธ์: {best['result']}"

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"[LOG] {action} {cipher_type} - Time: {elapsed_time:.6f}s")
    
    return jsonify({'result': result, 'time': elapsed_time})

if __name__ == '__main__':
    app.run(debug=True)

