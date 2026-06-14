import json 
import math
import re
from collections import Counter

from config import (
    CHUNKS_PATH,
    VECTOR_INDEX_PATH,
    TOP_K
) 


def tokenize(text):
    text = text.lower()

    tokens = re.findall(
        r"[a-zA-ZəöüğışçıƏÖÜĞIİŞÇ0-9-]+",
        text
    )
# Bu regex metinden kelimeleri çıkarır.
# Örnek:
# Layihənin test parolu “ALFA-27” olaraq qeyd olunub.
# çıktı:
# [
#   "layihənin",
#   "test",
#   "parolu",
#   "alfa-27",
#   "olaraq",
#   "qeyd",
#   "olunub"
# ]
# Yani nokta, tırnak, virgül gibi şeyleri atar; kelimeleri alır.

    return tokens



def create_vector(text):
    tokens = tokenize(text)

    vector = Counter(tokens)

    return dict(vector)
# Örnek:
# "test parolu test"
# tokenize sonrası:
# ["test", "parolu", "test"]
# Counter sonrası:
# {
#   "test": 2,
#   "parolu": 1
# }
# Yani sistem şunu öğreniyor:
# Bu metinde hangi kelime kaç defa geçiyor?




def cosine_similarity(vector_a, vector_b):
    common_words = set(vector_a.keys()) & set(vector_b.keys())

    dot_product = 0

    for word in common_words:
        dot_product += vector_a[word] * vector_b[word]

    norm_a = math.sqrt(
        sum(value ** 2 for value in vector_a.values())
    )

    norm_b = math.sqrt(
        sum(value **2 for value in vector_b.values())
    )

    if norm_a ==0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)
# cosine_similarity
# > soru ile chunk arasında ortak kelimelere bakar
# > benzerlik skoru hesaplar
# > en yüksek skor alan chunk en alakalı kabul edilir

# Mesela soru:
# Layihənin test parolu nədir?
# Chunk içinde:
# Layihənin test parolu ALFA-27-dir.



def load_chunks():
    chunks = []

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f'chunks file not found: {CHUNKS_PATH}')
    
    with open(CHUNKS_PATH, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
                chunks.append(chunk)

            except json.JSONDecodeError:
                print(f'skipped invalid JSON at {line_num}')
    
    return chunks
# chunks.jsonl dosyasını okur
# her satırı JSON olarak çevirir
# chunks listesine ekler
# en sonda chunks listesini döndürür



def build_vector_index():
    chunks = load_chunks()

    index_items = []

    for chunk in chunks:
        chunk_text = chunk['text']
        vector = create_vector(chunk_text)

        index_items.append({
            'chunk_id': chunk['chunk_id'],
            'text': chunk_text,
            'vector': vector
        })

    return index_items

# Chunk text:
# "Layihənin test parolu ALFA-27-dir."

# Kelime vektörü:
# {"layihənin": 1, "test": 1, "parolu": 1, "alfa-27-dir": 1}

# Arama index’i:
# chunk_id + text + vector



def save_vector_index(index_items):
    VECTOR_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(VECTOR_INDEX_PATH, 'w', encoding='utf-8') as file:
        json.dump(index_items, file, ensure_ascii=False, indent=2)



def load_vector_index():
    if not VECTOR_INDEX_PATH.exists():
        raise FileNotFoundError(f'vector index not found: {VECTOR_INDEX_PATH}')
    
    with open(VECTOR_INDEX_PATH, 'r', encoding='utf-8') as file:
        index_items = json.load(file)

    return index_items



def retrieve_top_chunks(question, top_k=TOP_K):
    index_items = load_vector_index()

    question_vector = create_vector(question)

    scored_chunks = []

    for item in index_items:
        score = cosine_similarity(question_vector, item['vector'])

        scored_chunks.append({
            'chunk_id': item['chunk_id'],
            'text': item['text'],
            'score': score
        })

    scored_chunks.sort(
        key=lambda item: item['score'],
        reverse=True
    )

    return scored_chunks[:top_k]
# 1. Arama index’ini okur
# 2. Soruyu kelime vektörüne çevirir
# 3. Soruyu her chunk ile karşılaştırır
# 4. Her chunk’a benzerlik skoru verir
# 5. Skoru yüksek olanları üste dizer
# 6. En iyi TOP_K chunk’ı döndürür


def main():
    index_items = build_vector_index()
    save_vector_index(index_items)

    print("Vector index built successfully.")
    print(f"Chunks indexed: {len(index_items)}")
    print(f"Saved to: {VECTOR_INDEX_PATH}")

    print("\nTest retrieval:")

    test_question = "Layihənin test parolu nədir?"
    results = retrieve_top_chunks(test_question)

    print(f"Question: {test_question}")

    for result in results:
        print("\n-------------------------")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Score: {round(result['score'], 4)}")
        print(result["text"])


if __name__ == "__main__":
    main()
