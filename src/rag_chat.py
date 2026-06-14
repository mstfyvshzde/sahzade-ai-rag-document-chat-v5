import json
import re
from datetime import datetime

from config import RAG_RESULTS_PATH, TOP_K
from retriever import retrieve_top_chunks, tokenize


def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            cleaned_sentences.append(sentence)

    return cleaned_sentences



def score_sentence(question, sentence):
    question_tokens = set(tokenize(question))
    sentence_tokens = set(tokenize(sentence))

    if not question_tokens or not sentence_tokens:
        return 0
    
    common_tokens = question_tokens & sentence_tokens # Ortak kelimeleri bulur:

    return len(common_tokens)



# Retrieve = bulup geri getirmek
def find_best_answer_sentence(question, retrieved_chunks):
    best_sentence = ''
    best_score = 0

    for chunk in retrieved_chunks:
        sentences = split_into_sentences(chunk['text'])

        for sentence in sentences:
            score = score_sentence(question, sentence)

            if score > best_score:
                best_score = score
                best_sentence = sentence
    
    if best_sentence: # En iyi cümle bulunduysa onu döndürür.
        return best_sentence

    return "Sənəddə bu suala uyğun dəqiq cavab tapılmadı."
# Soru geldi > Alakalı chunk’lar geldi > Chunk’lar cümlelere bölündü > Her cümle soruyla karşılaştırıldı > En yüksek skorlu cümle cevap seçildi




def save_rag_results(question, answer, retrieved_chunks):
    RAG_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    result_data = {
        'time': datetime.now().isoformat(),
        'question': question,
        'answer': answer,
        'top_k': TOP_K,
        'retrieved_chunks': [
            {
                'chunk_id': chunk['chunk_id'],
                'score': chunk['score'],
                'text': chunk['text']
            }
            for chunk in retrieved_chunks
        ]
    }

    with open(RAG_RESULTS_PATH, 'a', encoding='utf-8') as file:
        file.write(json.dumps(result_data, ensure_ascii=False) + '\n')



def ask_question(question):
    retrieved_chunks = retrieve_top_chunks(question)

    answer = find_best_answer_sentence(question, retrieved_chunks)

    save_rag_results(question, answer, retrieved_chunks)

    return answer, retrieved_chunks




def run_rag_chat():
    print("Sahzade AI RAG Document Chat V5")
    print("--------------------------------")
    print("Type your question.")
    print("Type 'q' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() == "q":
            print("RAG chat stopped.")
            break

        if not question:
            continue

        answer, retrieved_chunks = ask_question(question)

        print("\nAnswer:")
        print(answer)

        print("\nRetrieved chunks:")
        for chunk in retrieved_chunks:
            print("-------------------------")
            print(f"Chunk ID: {chunk['chunk_id']}")
            print(f"Score: {round(chunk['score'], 4)}")

        print("\n")


if __name__ == "__main__":
    run_rag_chat()