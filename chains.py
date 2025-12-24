from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def get_rag_chain(llm, retriever):
    prompt = PromptTemplate(
        template="""
        Answer ONLY from the context.
        If not found, say "I don't know".

        Context:
        {context}

        Question:
        {question}

        Answer:
        """,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
