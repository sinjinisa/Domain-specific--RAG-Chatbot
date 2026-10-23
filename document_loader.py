from io import BytesIO

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

MAX_FILES = 5
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_PAGES = 100


def load_documents(uploaded_files):
    """Return PDF chunks with filenames and page numbers."""

    if not uploaded_files:
        raise ValueError("Upload at least one PDF.")

    if len(uploaded_files) > MAX_FILES:
        raise ValueError(
            f"You may upload a maximum of {MAX_FILES} PDFs."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=130,
    )

    chunks = []
    total_pages = 0
    readable_pages = 0

    for uploaded_file in uploaded_files:

        if not uploaded_file.name.lower().endswith(".pdf"):
            raise ValueError(
                f"Not a PDF: {uploaded_file.name}"
            )

        pdf_bytes = uploaded_file.getvalue()

        if len(pdf_bytes) > MAX_FILE_BYTES:
            raise ValueError(
                f"{uploaded_file.name} is larger than 10 MB."
            )

        try:
            reader = PdfReader(BytesIO(pdf_bytes))

            if reader.is_encrypted:
                raise ValueError(
                    f"{uploaded_file.name} is password protected."
                )

            total_pages += len(reader.pages)

            if total_pages > MAX_TOTAL_PAGES:
                raise ValueError(
                    "Upload at most 100 pages in total."
                )

            for page_number, page in enumerate(
                reader.pages, start=1
            ):

                text = (page.extract_text() or "").strip()

                if not text:
                    continue

                readable_pages += 1

                for part_number, part in enumerate(
                    splitter.split_text(text), start=1
                ):

                    chunks.append(
                        {
                            "text": part,
                            "source": uploaded_file.name,
                            "page": page_number,
                            "part": part_number,
                        }
                    )

        except ValueError:
            raise

        except Exception as error:
            raise ValueError(
                f"Could not read {uploaded_file.name}: {error}"
            ) from error

    if not chunks:
        raise ValueError(
            "No selectable text was found. "
            "Try a text-based PDF, not a scan."
        )

    return chunks, readable_pages