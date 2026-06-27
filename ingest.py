from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


DATA_DIR = "data"
CHROMA_DIR = "chroma_db"


def load_documents():

    documents = []

    for file_path in Path(DATA_DIR).glob("*.txt"):

        print(f"Loading: {file_path}")

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def create_vector_store(chunks):

    embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR
        )

    print(f"\nStored {len(chunks)} chunks in Chroma")


def main():

    documents = load_documents()

    print(f"\nLoaded {len(documents)} documents")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    create_vector_store(chunks)

    print("\nIngestion Complete")


if __name__ == "__main__":
    main()