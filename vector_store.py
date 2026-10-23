import faiss
import numpy as np
import streamlit as st

from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


@st.cache_resource(
    show_spinner="Loading the embedding model..."
)
def get_embedding_model():

    return SentenceTransformer(EMBEDDING_MODEL)


def create_index(chunks):

    model = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    vectors = np.ascontiguousarray(
        embeddings,
        dtype=np.float32
    )

    index = faiss.IndexFlatIP(vectors.shape[1])

    index.add(vectors)

    return index


def retrieve(
    question,
    index,
    chunks,
    top_k=4,
    min_score=0.25
):

    model = get_embedding_model()

    embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    query_vector = np.ascontiguousarray(
        embedding,
        dtype=np.float32
    )

    scores, positions = index.search(
        query_vector,
        min(top_k, index.ntotal)
    )

    matches = []

    for score, position in zip(
        scores[0],
        positions[0]
    ):

        if position < 0 or float(score) < min_score:
            continue

        matches.append(
            {
                **chunks[int(position)],
                "score": float(score)
            }
        )

    return matches