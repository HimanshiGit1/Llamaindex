# -*- coding: utf-8 -*-
"""ingestiondata.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vggz_T8Lsa4Tvo0b6Eg8OKpgzwK16Pcc
"""

!pip install python-dotenv

!pip install llama-index

!pip install llama-index-llms-ollama

!pip install llama-index-embeddings-huggingface

# Install the specific LlamaIndex integration for Pinecone vector stores
!pip install llama-index-vector-stores-pinecone

from dotenv import load_dotenv
import os
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

!pip install unstructured

from google.colab import drive
drive.mount('/content/drive')

if __name__ == "__main__":
    print("Going to ingest pinecone documentation...")
    from llama_index.readers.file import UnstructuredReader

    dir_reader = SimpleDirectoryReader(
        input_dir="/content/drive/MyDrive/Llamaindex/llamaindex-docs",
        file_extractor={".html": UnstructuredReader()},
    )
    documents = dir_reader.load_data()
    node_parser = SimpleNodeParser.from_defaults(chunk_size=500, chunk_overlap=20)

    #llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
    #embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)

    #Settings.llm = OpenAI()
    #Settings.embed_model = OpenAIEmbedding()
    llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
    Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5")

    index_name = "llamaindex-docs-index"
    pc = Pinecone(api_key="pcsk_6Av3iw_6qHBCwXBXEaQJHGgZTCCBrq7KAhoE1pvwZWNn5NewW6t3LiR6sQgBH39c6GjYsU")

    # Check if index exists and delete if it does
    # if index_name in pc.list_indexes():
    #     print(f"Deleting existing index: {index_name}")
    #     pc.delete_index(index_name)
    #     print(f"Index {index_name} deleted.")

    # Create index if it doesn't exist with the correct dimension
    # Get the embedding dimension from the HuggingFace model
    # embedding_dimension = Settings.embed_model.get_text_embedding
    # if index_name not in pc.list_indexes():
    #     print(f"Creating new index: {index_name} with dimension {embedding_dimension}")
    #     pc.create_index(name=index_name, dimension=embedding_dimension, metric="cosine")
    #     print(f"Index {index_name} created.")

    pinecone_index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        show_progress=True,
    )
    print("finished ingesting...")