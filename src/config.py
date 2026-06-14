from pathlib import Path


# Projenin ana klasörünü bulur.
BASE_DIR = Path(__file__).resolve().parents[1]

# data klasörünün yolunu tutar.
DATA_DIR = BASE_DIR / "data"


DOCUMENTS_DIR = DATA_DIR / "documents" # Asıl belgelerin durduğu klasör.
CHUNKS_DIR = DATA_DIR / "chunks" # Belge parçalarının kaydedileceği klasör.
INDEX_DIR = DATA_DIR / "index" # Arama index dosyasının kaydedileceği klasör.

OUTPUTS_DIR = BASE_DIR / "outputs"


DOCUMENT_PATH = DOCUMENTS_DIR / "sample_document.txt" # Okunacak ana TXT belgesinin tam yolu.

CHUNKS_PATH = CHUNKS_DIR / "chunks.jsonl" # Belge parçalandıktan sonra parçaların yazılacağı dosya.

VECTOR_INDEX_PATH = INDEX_DIR / "vector_index.json" # Arama için oluşturulacak index dosyası

RAG_RESULTS_PATH = OUTPUTS_DIR / "rag_results.txt"



# Chunk = belgenin küçük parçasıdir.
# Örnek belge:
# Şahzadə Qülləsinin gizli kod adı Mavi Qapıdır. Layihənin test parolu ALFA-27-dir.

# Parçalara bölünür:
# Chunk 1:
# Şahzadə Qülləsinin gizli kod adı Mavi Qapıdır.

# Chunk 2:
# Layihənin test parolu ALFA-27-dir.

# Soru:
# Layihənin test parolu nədir?
# Sistem Chunk 2’yi bulur ve cevap verir:
# Test parolu ALFA-27-dir.

CHUNK_SIZE = 450 
# Her parçanın yaklaşık kaç karakter olacağını söyler.
# Küçük chunk -> daha net arama
# Büyük chunk -> daha fazla bağlam



CHUNK_OVERLAP = 80 
# Chunk’lar arasında tekrar bırakır.
# Neden? Bilgi iki parçanın arasında bölünmesin diye.
# Kötü bölünme:
# Chunk 1: Layihənin rəhbəri Elvin
# Chunk 2: Rəhimlidir.
# Overlap olursa:
# Chunk 1: Layihənin rəhbəri Elvin Rəhimlidir.
# Chunk 2: Elvin Rəhimlidir. Texniki köməkçi...


TOP_K = 3
# Soru sorulunca en alakalı kaç parça getirilecek onu belirler.