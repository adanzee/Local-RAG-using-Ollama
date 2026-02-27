# only contain chunking logic and related helper functions


def chunk_text(text, chunk_size=500, overlap=50):
    # Simple chinking function that splits text into 500 chunk size
    all_chunks = []
    start = 0
    while start < len(text):
        # end point of chunk
        end = start + chunk_size

        # it is to deal with the if we are in the in the mid of text and chunk_size limit hit
        if end < len(text):
            # .rfind  search backward for the last occurence
            # rfind()= reverse find, to check if the chunk ends in the middle of word
            smart_end = text.rfind(" ", start, end)

            # if the space is find move the end point to the last space
            if smart_end != -1 and smart_end > start:
                end = smart_end

        current_chunk = text[start:end].strip()

        if current_chunk:
            all_chunks.append(current_chunk)

        start = end - overlap

        if start >= len(text) or end >= len(text):
            break

    return all_chunks
