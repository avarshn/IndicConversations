from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_chunks(content, source_url):
    document = Document(
        page_content=content, metadata={"source": source_url}
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=200, 
        add_start_index=True, # track index in original document
        separators=["\n\n==", "\n\n", "\n", ". ", " ", ""],  # prioritize section headers
        length_function=len,
    )

    all_splits = text_splitter.split_documents([document])

    return all_splits

def merge_small_documents_with_metadata(docs, min_size=150):
    """Merge small documents while preserving important metadata"""
    merged = []
    i = 0
    
    while i < len(docs):
        current_doc = docs[i]
        current_content = current_doc.page_content.strip()
        
        if len(current_content) < min_size and i + 1 < len(docs):
            # Merge content
            merged_content = current_content + "\n\n" + docs[i + 1].page_content
            
            # Merge metadata intelligently
            merged_metadata = current_doc.metadata.copy()
            
            merged_doc = Document(
                page_content=merged_content,
                metadata=merged_metadata
            )
            merged.append(merged_doc)
            i += 2
        else:
            merged.append(current_doc)
            i += 1
    
    return merged