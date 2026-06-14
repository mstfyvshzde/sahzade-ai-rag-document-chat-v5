from config import DOCUMENT_PATH

def load_documnet():
    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(f'focumnet not found: {DOCUMENT_PATH}')
    
    with open(DOCUMENT_PATH, 'r', encoding='utf-8') as file:
        text = file.read()

    return text.strip()



def main():
    document_text = load_documnet()

    print("Document loaded successfully.")
    print(f"Document path: {DOCUMENT_PATH}")
    print(f"Character count: {len(document_text)}")

    print("\nPreview:")
    print(document_text[:300])


if __name__ == "__main__":
    main()