import json
 
from config import (
    DOCUMENT_PATH,
    CHUNKS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def load_text():
    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(f'documents not found: {DOCUMENT_PATH}')
    
    with open(DOCUMENT_PATH, 'r', encoding='utf-8') as file:
        text = file.read()

    return text.strip()


def split_text_into_chunks(text):
    chunks = []
    start = 0 # metnin nereden kesilmeye başlanacağını gösterir.
    chunk_id = 1 # her parçaya numara verir.
    
    
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()
# Burada metinden bir parça kesilir.
# Örnek:
# CHUNK_SIZE = 10
# text = "Salam dostum necesen"
# İlk parça:
# Salam dost
# Çünkü 0’dan 10 karaktere kadar alır.


        if chunk_text: # Eğer parça boş değilse listeye ekler.
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text
            })

        chunk_id += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
# Örnek:
# CHUNK_SIZE = 100
# CHUNK_OVERLAP = 20
# O zaman:
# start += 80
# Yani yeni chunk 100 karakter sonra değil, 80 karakter sonra başlar.
# Böylece iki chunk arasında 20 karakter tekrar olur.
# Örnek:
# Chunk 1: karakter 0–100
# Chunk 2: karakter 80–180
# Chunk 3: karakter 160–260
# Yani 80–100 arası hem Chunk 1’de hem Chunk 2’de var

    return chunks




def save_chunks(chunks):
    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CHUNKS_PATH, 'w', encoding='utf-8') as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + '\n')



def main():
    text = load_text()
    chunks = split_text_into_chunks(text)
    save_chunks(chunks)

    print("Document chunking completed.")
    print(f"Source document: {DOCUMENT_PATH}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved to: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()