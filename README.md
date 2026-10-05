\# Enterprise AI Copilot — Intelligent Knowledge \& Data Assistant



An enterprise-focused Generative AI application that combines RAG, SQL, NoSQL, LLM tool routing, REST APIs, and Docker.



\## Key Features



\- Retrieval-Augmented Generation (RAG)

\- Hugging Face sentence-transformer embeddings

\- ChromaDB vector database

\- Llama 3.2 using Ollama

\- LangChain tool-based agent

\- SQLite SQL database

\- MongoDB NoSQL database

\- FastAPI REST API

\- Streamlit user interface

\- Docker containerization

\- Automated testing with Pytest



\## Architecture



```text

User

&#x20; |

&#x20; v

Streamlit UI

&#x20; |

&#x20; v

FastAPI REST API

&#x20; |

&#x20; v

LangChain Agent

&#x20; |

&#x20; +----> RAG + ChromaDB

&#x20; |

&#x20; +----> SQLite

&#x20; |

&#x20; +----> MongoDB

&#x20; |

&#x20; v

Llama 3.2 / Ollama

