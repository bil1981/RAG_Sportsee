Downloading openai-3.3.0-py3-none-any.whl (1.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 4.8 MB/s  0:00:00
Installing collected packages: jiter, openai, instructor
  Attempting uninstall: jiter
    Found existing installation: jiter 0.17.0
    Uninstalling jiter-0.17.0:
      Successfully uninstalled jiter-0.17.0
  Attempting uninstall: openai
    Found existing installation: openai 1.109.1
    Uninstalling openai-1.109.1:
      Successfully uninstalled openai-1.109.1
  Attempting uninstall: instructor
    Found existing installation: instructor 1.3.2
    Uninstalling instructor-1.3.2:
      Successfully uninstalled instructor-1.3.2
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
langchain-openai 1.1.9 requires openai<3.0.0,>=1.109.1, but you have openai 3.3.0 which is incompatible.
Successfully installed instructor-1.17.0 jiter-0.14.0 openai-3.3.0
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip show instructor
Name: instructor
Version: 1.17.0
Summary: structured outputs for llm
Home-page: 
Author: Jason Liu, Ivan Leo
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: aiohttp, click, docstring-parser, idna, jinja2, jiter, openai, pydantic, pydantic-core, regex, requests, rich, tenacity, typer, urllib3
Required-by: ragas
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas; print('RAGAS OK:', ragas.__version__)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas.llms; print('LLM module OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas.embeddings; print('Embeddings module OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> ollama run llama3.1:latest "Réponds simplement : Ollama fonctionne."
Je suis désolé, mais je n'ai pas compris votre question. Pouvez-vous répéter ou préciser ce que vous voulez 
savoir sur Ollama ?

(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip install ollama
Requirement already satisfied: ollama in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (0.6.3)
Requirement already satisfied: httpx>=0.27 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from ollama) (0.28.1)
Requirement already satisfied: pydantic>=2.9 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from ollama) (2.13.5)
Requirement already satisfied: anyio in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx>=0.27->ollama) (4.15.1)
Requirement already satisfied: certifi in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx>=0.27->ollama) (2026.7.22)
Requirement already satisfied: httpcore==1.* in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx>=0.27->ollama) (1.0.9)
Requirement already satisfied: idna in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx>=0.27->ollama) (3.20)
Requirement already satisfied: h11>=0.16 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpcore==1.*->httpx>=0.27->ollama) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic>=2.9->ollama) (0.8.0)
Requirement already satisfied: pydantic-core==2.46.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic>=2.9->ollama) (2.46.5)
Requirement already satisfied: typing-extensions>=4.14.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic>=2.9->ollama) (4.16.0)
Requirement already satisfied: typing-inspection>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic>=2.9->ollama) (0.4.4)
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip install --upgrade instructor
Requirement already satisfied: instructor in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (1.17.0)
Requirement already satisfied: aiohttp<4.0.0,>=3.14.3 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (3.14.3)
Requirement already satisfied: click>=8.3.3 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (8.5.0)
Requirement already satisfied: docstring-parser<1.0,>=0.16 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (0.16)
Requirement already satisfied: idna>=3.15 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (3.20)
Requirement already satisfied: jinja2<4.0.0,>=3.1.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (3.1.6)
Requirement already satisfied: jiter<0.15,>=0.6.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (0.14.0)
Requirement already satisfied: openai<4.0.0,>=2.0.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (3.3.0)
Requirement already satisfied: pydantic-core<3.0.0,>=2.18.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (2.46.5)
Requirement already satisfied: pydantic<3.0.0,>=2.8.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (2.13.5)
Requirement already satisfied: regex<2027.0.0,>=2023.0.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (2026.9.10)
Requirement already satisfied: requests<3.0.0,>=2.33.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (2.34.2)
Requirement already satisfied: rich<15.0.0,>=13.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (13.9.4)
Requirement already satisfied: tenacity<10.0.0,>=8.2.3 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (8.5.0)
Requirement already satisfied: typer<1.0.0,>=0.9.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (0.27.2)
Requirement already satisfied: urllib3<3.0.0,>=2.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from instructor) (2.7.0)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (6.8.0)
Requirement already satisfied: propcache>=0.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (0.5.4)
Requirement already satisfied: typing_extensions>=4.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.14.3->instructor) (1.25.1)
Requirement already satisfied: MarkupSafe>=2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from jinja2<4.0.0,>=3.1.4->instructor) (3.0.3)
Requirement already satisfied: anyio<5,>=4.10.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from openai<4.0.0,>=2.0.0->instructor) (4.15.1)
Requirement already satisfied: distro<2,>=1.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from openai<4.0.0,>=2.0.0->instructor) (1.9.0)
Requirement already satisfied: httpx2<3,>=2.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from openai<4.0.0,>=2.0.0->instructor) (2.13.1)
Requirement already satisfied: sniffio in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from openai<4.0.0,>=2.0.0->instructor) (1.3.1)
Requirement already satisfied: httpcore2==2.13.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2.7.0->openai<4.0.0,>=2.0.0->instructor) (2.13.1)
Requirement already satisfied: truststore>=0.10 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2.7.0->openai<4.0.0,>=2.0.0->instructor) (0.10.4)
Requirement already satisfied: h11>=0.16 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpcore2==2.13.1->httpx2<3,>=2.7.0->openai<4.0.0,>=2.0.0->instructor) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.8.0->instructor) (0.8.0)
Requirement already satisfied: typing-inspection>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.8.0->instructor) (0.4.4)
Requirement already satisfied: charset_normalizer<4,>=2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.33.0->instructor) (3.5.1)
Requirement already satisfied: certifi>=2023.5.7 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.33.0->instructor) (2026.7.22)
Requirement already satisfied: markdown-it-py>=2.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from rich<15.0.0,>=13.7.0->instructor) (4.2.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from rich<15.0.0,>=13.7.0->instructor) (2.21.0)
Requirement already satisfied: shellingham>=1.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from typer<1.0.0,>=0.9.0->instructor) (1.5.4)
Requirement already satisfied: annotated-doc>=0.0.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from typer<1.0.0,>=0.9.0->instructor) (0.0.5)
Requirement already satisfied: colorama in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from typer<1.0.0,>=0.9.0->instructor) (0.4.6)
Requirement already satisfied: mdurl~=0.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from markdown-it-py>=2.2.0->rich<15.0.0,>=13.7.0->instructor) (0.1.2)
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas; print('RAGAS OK:', ragas.__version__); import ollama; print('OLLAMA OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\eval_ragas_ollama2.py        
Traceback (most recent call last):                                                                            
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\eval_ragas_ollama2.py", line 48, in <module>
    from ragas.dataset_schema import SingleTurnSample
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\eval_ragas_ollama2.py
Traceback (most recent call last):
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\eval_ragas_ollama2.py", line 48, in <module>
    from ragas.dataset_schema import SingleTurnSample
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\__init__.py", line 5, in <module>
    from ragas.evaluation import aevaluate, evaluate
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\evaluation.py", line 31, in <module>
    from ragas.llms import llm_factory
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\__init__.py", line 1, in <module>
    from ragas.llms.base import (
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages\ragas\llms\base.py", line 12, in <module>
    from langchain_community.chat_models.vertexai import ChatVertexAI
ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> 
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip show langchain langchain-core langchain-community langchain-openai instructor openai
Name: langchain
Version: 1.4.2
Summary: Building applications with LLMs through composability
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: langchain-core, langgraph, pydantic
Required-by: ragas
---
Name: langchain-core
Version: 1.6.4
Summary: Building applications with LLMs through composability
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: httpx, jsonpatch, langchain-protocol, langsmith, packaging, pydantic, pyyaml, tenacity, typing-extensions, uuid-utils
Required-by: langchain, langchain-classic, langchain-community, langchain-openai, langchain-text-splitters, langgraph, langgraph-checkpoint, langgraph-prebuilt, langgraph-sdk, ragas
---
Name: langchain-community
Version: 0.4.2
Summary: Community contributed LangChain integrations.
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: aiohttp, httpx-sse, langchain-classic, langchain-core, langsmith, numpy, pydantic-settings, pyyaml, requests, sqlalchemy, tenacity
Required-by: ragas
---
Name: langchain-openai
Version: 1.1.9
Summary: An integration package connecting OpenAI and LangChain
Home-page: https://docs.langchain.com/oss/python/integrations/providers/openai
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: langchain-core, openai, tiktoken
Required-by: ragas
---
Name: instructor
Version: 1.17.0
Summary: structured outputs for llm
Home-page: 
Author: Jason Liu, Ivan Leo
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: aiohttp, click, docstring-parser, idna, jinja2, jiter, openai, pydantic, pydantic-core, regex, requests, rich, tenacity, typer, urllib3
Required-by: ragas
---
Name: openai
Version: 3.3.0
Summary: The official Python library for the openai API
Home-page: https://github.com/openai/openai-python
Author: 
Author-email: OpenAI <support@openai.com>
License: Apache-2.0
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: anyio, distro, httpx2, jiter, pydantic, sniffio, typing-extensions
Required-by: instructor, langchain-openai, ragas
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip show langchain langchain-core langchain-community langchain-openai instructor openai
Name: langchain
Version: 1.4.2
Summary: Building applications with LLMs through composability
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: langchain-core, langgraph, pydantic
Required-by: ragas
---
Name: langchain-core
Version: 1.6.4
Summary: Building applications with LLMs through composability
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: httpx, jsonpatch, langchain-protocol, langsmith, packaging, pydantic, pyyaml, tenacity, typing-extensions, uuid-utils
Required-by: langchain, langchain-classic, langchain-community, langchain-openai, langchain-text-splitters, langgraph, langgraph-checkpoint, langgraph-prebuilt, langgraph-sdk, ragas
---
Name: langchain-community
Version: 0.4.2
Summary: Community contributed LangChain integrations.
Home-page: https://docs.langchain.com/
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: aiohttp, httpx-sse, langchain-classic, langchain-core, langsmith, numpy, pydantic-settings, pyyaml, requests, sqlalchemy, tenacity
Required-by: ragas
---
Name: langchain-openai
Version: 1.1.9
Summary: An integration package connecting OpenAI and LangChain
Home-page: https://docs.langchain.com/oss/python/integrations/providers/openai
Author: 
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: langchain-core, openai, tiktoken
Required-by: ragas
---
Name: instructor
Version: 1.17.0
Summary: structured outputs for llm
Home-page: 
Author: Jason Liu, Ivan Leo
Author-email: 
License: MIT
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: aiohttp, click, docstring-parser, idna, jinja2, jiter, openai, pydantic, pydantic-core, regex, requests, rich, tenacity, typer, urllib3
Required-by: ragas
---
Name: openai
Version: 3.3.0
Summary: The official Python library for the openai API
Home-page: https://github.com/openai/openai-python
Author: 
Author-email: OpenAI <support@openai.com>
License: Apache-2.0
Location: C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages
Requires: anyio, distro, httpx2, jiter, pydantic, sniffio, typing-extensions
Required-by: instructor, langchain-openai, ragas
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> 
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip install "langchain-community==0.3.31"
Collecting langchain-community==0.3.31
  Using cached langchain_community-0.3.31-py3-none-any.whl.metadata (3.0 kB)
Requirement already satisfied: langchain-core<2.0.0,>=0.3.78 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (1.6.4)
Requirement already satisfied: langchain<2.0.0,>=0.3.27 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (1.4.2)
Requirement already satisfied: SQLAlchemy<3.0.0,>=1.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.0.54)
Requirement already satisfied: requests<3.0.0,>=2.32.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.34.2)
Requirement already satisfied: PyYAML<7.0.0,>=5.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (6.0.3)
Requirement already satisfied: aiohttp<4.0.0,>=3.8.3 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (3.14.3)
Requirement already satisfied: tenacity!=8.4.0,<10.0.0,>=8.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (8.5.0)
Collecting dataclasses-json<0.7.0,>=0.6.7 (from langchain-community==0.3.31)
  Using cached dataclasses_json-0.6.7-py3-none-any.whl.metadata (25 kB)
Requirement already satisfied: pydantic-settings<3.0.0,>=2.10.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.15.0)
Requirement already satisfied: langsmith<1.0.0,>=0.1.125 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (0.14.0)
Requirement already satisfied: httpx-sse<1.0.0,>=0.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (0.4.3)
Requirement already satisfied: numpy>=1.26.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.5.3)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (6.8.0)
Requirement already satisfied: propcache>=0.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (0.5.4)
Requirement already satisfied: typing_extensions>=4.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.25.1)
Collecting marshmallow<4.0.0,>=3.18.0 (from dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31)
  Using cached marshmallow-3.26.2-py3-none-any.whl.metadata (7.3 kB)
Requirement already satisfied: typing-inspect<1,>=0.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31) (0.9.0)
Requirement already satisfied: langgraph<1.3.0,>=1.2.11 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.2.12)
Requirement already satisfied: pydantic<3.0.0,>=2.7.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (2.13.5)
Requirement already satisfied: httpx<1.0.0,>=0.23.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.28.1)
Requirement already satisfied: jsonpatch<2.0.0,>=1.33.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (1.33)
Requirement already satisfied: langchain-protocol>=0.0.17 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.0.19)
Requirement already satisfied: packaging>=23.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (26.3)
Requirement already satisfied: uuid-utils<1.0,>=0.12.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.17.1)
Requirement already satisfied: anyio in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (4.15.1)
Requirement already satisfied: certifi in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (2026.7.22)
Requirement already satisfied: httpcore==1.* in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (1.0.9)
Requirement already satisfied: idna in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (3.20)
Requirement already satisfied: h11>=0.16 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpcore==1.*->httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.16.0)
Requirement already satisfied: jsonpointer>=1.9 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from jsonpatch<2.0.0,>=1.33.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (3.1.1)
Requirement already satisfied: langgraph-checkpoint<5.0.0,>=4.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (4.2.0)
Requirement already satisfied: langgraph-prebuilt<1.2.0,>=1.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.1.0)
Requirement already satisfied: langgraph-sdk<0.5.0,>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.4.5)
Requirement already satisfied: xxhash>=3.5.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (4.0.1)
Requirement already satisfied: ormsgpack>=1.12.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-checkpoint<5.0.0,>=4.1.0->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.12.2)
Requirement already satisfied: orjson>=3.11.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-sdk<0.5.0,>=0.4.2->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (3.12.0)
Requirement already satisfied: websockets<17,>=14 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-sdk<0.5.0,>=0.4.2->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (16.1.1)
Requirement already satisfied: distro>=1.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.9.0)
Requirement already satisfied: httpx2<3,>=2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (2.13.1)
Requirement already satisfied: requests-toolbelt>=1.0.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.0.0)
Requirement already satisfied: sniffio>=1.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.3.1)
Requirement already satisfied: zstandard>=0.23.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (0.25.0)
Requirement already satisfied: httpcore2==2.13.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2->langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (2.13.1)
Requirement already satisfied: truststore>=0.10 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2->langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (0.10.4)
Requirement already satisfied: annotated-types>=0.6.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.8.0)
Requirement already satisfied: pydantic-core==2.46.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (2.46.5)
Requirement already satisfied: typing-inspection>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.4.4)
Requirement already satisfied: python-dotenv>=0.21.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic-settings<3.0.0,>=2.10.1->langchain-community==0.3.31) (1.2.3)
Requirement already satisfied: charset_normalizer<4,>=2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.5->langchain-community==0.3.31) (3.5.1)
Requirement already satisfied: urllib3<3,>=1.26 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.5->langchain-community==0.3.31) (2.7.0)
Requirement already satisfied: greenlet>=1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from SQLAlchemy<3.0.0,>=1.4.0->langchain-community==0.3.31) (3.5.6)
Requirement already satisfied: mypy-extensions>=0.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from typing-inspect<1,>=0.4.0->dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31) (1.1.0)
Using cached langchain_community-0.3.31-py3-none-any.whl (2.5 MB)
Using cached dataclasses_json-0.6.7-py3-none-any.whl (28 kB)
Using cached marshmallow-3.26.2-py3-none-any.whl (50 kB)
Installing collected packages: marshmallow, dataclasses-json, langchain-community
  Attempting uninstall: langchain-community
    Found existing installation: langchain-community 0.4.2
    Uninstalling langchain-community-0.4.2:
      Successfully uninstalled langchain-community-0.4.2
Successfully installed dataclasses-json-0.6.7 langchain-community-0.3.31 marshmallow-3.26.2
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas; print('RAGAS OK:', ragas.__version__)"
RAGAS OK: 0.4.3
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ollama; print('OLLAMA OK')"
OLLAMA OK
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -m pip install "langchain-community==0.3.31"
Requirement already satisfied: langchain-community==0.3.31 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (0.3.31)
Requirement already satisfied: langchain-core<2.0.0,>=0.3.78 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (1.6.4)
Requirement already satisfied: langchain<2.0.0,>=0.3.27 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (1.4.2)
Requirement already satisfied: SQLAlchemy<3.0.0,>=1.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.0.54)
Requirement already satisfied: requests<3.0.0,>=2.32.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.34.2)
Requirement already satisfied: PyYAML<7.0.0,>=5.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (6.0.3)
Requirement already satisfied: aiohttp<4.0.0,>=3.8.3 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (3.14.3)
Requirement already satisfied: tenacity!=8.4.0,<10.0.0,>=8.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (8.5.0)
Requirement already satisfied: dataclasses-json<0.7.0,>=0.6.7 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (0.6.7)
Requirement already satisfied: pydantic-settings<3.0.0,>=2.10.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.15.0)
Requirement already satisfied: langsmith<1.0.0,>=0.1.125 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (0.14.0)
Requirement already satisfied: httpx-sse<1.0.0,>=0.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (0.4.3)
Requirement already satisfied: numpy>=1.26.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-community==0.3.31) (2.5.3)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (6.8.0)
Requirement already satisfied: propcache>=0.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (0.5.4)
Requirement already satisfied: typing_extensions>=4.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community==0.3.31) (1.25.1)
Requirement already satisfied: marshmallow<4.0.0,>=3.18.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31) (3.26.2)
Requirement already satisfied: typing-inspect<1,>=0.4.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31) (0.9.0)
Requirement already satisfied: langgraph<1.3.0,>=1.2.11 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.2.12)
Requirement already satisfied: pydantic<3.0.0,>=2.7.4 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (2.13.5)
Requirement already satisfied: httpx<1.0.0,>=0.23.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.28.1)
Requirement already satisfied: jsonpatch<2.0.0,>=1.33.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (1.33)
Requirement already satisfied: langchain-protocol>=0.0.17 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.0.19)
Requirement already satisfied: packaging>=23.2.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (26.3)
Requirement already satisfied: uuid-utils<1.0,>=0.12.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.17.1)
Requirement already satisfied: anyio in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (4.15.1)
Requirement already satisfied: certifi in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (2026.7.22)
Requirement already satisfied: httpcore==1.* in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (1.0.9)
Requirement already satisfied: idna in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (3.20)
Requirement already satisfied: h11>=0.16 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpcore==1.*->httpx<1.0.0,>=0.23.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (0.16.0)
Requirement already satisfied: jsonpointer>=1.9 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from jsonpatch<2.0.0,>=1.33.0->langchain-core<2.0.0,>=0.3.78->langchain-community==0.3.31) (3.1.1)
Requirement already satisfied: langgraph-checkpoint<5.0.0,>=4.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (4.2.0)
Requirement already satisfied: langgraph-prebuilt<1.2.0,>=1.1.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.1.0)
Requirement already satisfied: langgraph-sdk<0.5.0,>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.4.5)
Requirement already satisfied: xxhash>=3.5.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (4.0.1)
Requirement already satisfied: ormsgpack>=1.12.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-checkpoint<5.0.0,>=4.1.0->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (1.12.2)
Requirement already satisfied: orjson>=3.11.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-sdk<0.5.0,>=0.4.2->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (3.12.0)
Requirement already satisfied: websockets<17,>=14 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langgraph-sdk<0.5.0,>=0.4.2->langgraph<1.3.0,>=1.2.11->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (16.1.1)
Requirement already satisfied: distro>=1.7.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.9.0)
Requirement already satisfied: httpx2<3,>=2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (2.13.1)
Requirement already satisfied: requests-toolbelt>=1.0.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.0.0)
Requirement already satisfied: sniffio>=1.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (1.3.1)
Requirement already satisfied: zstandard>=0.23.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (0.25.0)
Requirement already satisfied: httpcore2==2.13.1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2->langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (2.13.1)
Requirement already satisfied: truststore>=0.10 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from httpx2<3,>=2->langsmith<1.0.0,>=0.1.125->langchain-community==0.3.31) (0.10.4)
Requirement already satisfied: annotated-types>=0.6.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.8.0)
Requirement already satisfied: pydantic-core==2.46.5 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (2.46.5)
Requirement already satisfied: typing-inspection>=0.4.2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.7.4->langchain<2.0.0,>=0.3.27->langchain-community==0.3.31) (0.4.4)
Requirement already satisfied: python-dotenv>=0.21.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from pydantic-settings<3.0.0,>=2.10.1->langchain-community==0.3.31) (1.2.3)
Requirement already satisfied: charset_normalizer<4,>=2 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.5->langchain-community==0.3.31) (3.5.1)
Requirement already satisfied: urllib3<3,>=1.26 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from requests<3.0.0,>=2.32.5->langchain-community==0.3.31) (2.7.0)
Requirement already satisfied: greenlet>=1 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from SQLAlchemy<3.0.0,>=1.4.0->langchain-community==0.3.31) (3.5.6)
Requirement already satisfied: mypy-extensions>=0.3.0 in C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv\Lib\site-packages (from typing-inspect<1,>=0.4.0->dataclasses-json<0.7.0,>=0.6.7->langchain-community==0.3.31) (1.1.0)
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python -c "import ragas; print('RAGAS OK:', ragas.__version__)"
RAGAS OK: 0.4.3
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\eval_ragas_ollama2.py        
                                                            

================================================================================
ÉVALUATION RAGAS 0.4.3 + OLLAMA
================================================================================

Configuration :
  RAGAS       : 0.4.3
  LLM         : llama3.1:latest
  Embeddings  : nomic-embed-text:latest
  Ollama      : http://localhost:11434
================================================================================
TEST DE CONNEXION OLLAMA
================================================================================

LLM        : llama3.1:latest
Embeddings : nomic-embed-text:latest
URL        : http://localhost:11434

[1/2] Test du LLM Ollama...
      OK
      Réponse : 'OLLAMA_TEST_OK'

[2/2] Test des embeddings Ollama...
      OK
      Dimension du vecteur : 768

Ollama est opérationnel.

================================================================================
INITIALISATION DES MÉTRIQUES RAGAS
================================================================================
  ✓ context_precision
  ✓ context_recall
  ✓ faithfulness
  ✓ response_relevancy
  ✓ answer_similarity


================================================================================
ÉVALUATION DU DATASET
================================================================================

TEST 1/3
      → context_precision... OK (1.0000)
      → context_recall... OK (1.0000)
      → faithfulness... OK (1.0000)
      → response_relevancy... OK (0.8758)
      → answer_similarity... ERREUR : AttributeError: 'OllamaRagasEmbeddings' object has no attribute 'run_config'

TEST 2/3
      → context_precision... OK (1.0000)
      → context_recall... OK (1.0000)
      → faithfulness... OK (1.0000)
      → response_relevancy... ERREUR : OutputParserException: Invalid json output: Combien de points concède l\'équipe lorsqu\'elle joue à domicile?
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 
      → answer_similarity... ERREUR : AttributeError: 'OllamaRagasEmbeddings' object has no attribute 'run_config'

TEST 3/3
      → context_precision... OK (0.0000)
      → context_recall... OK (1.0000)
      → faithfulness... OK (1.0000)
      → response_relevancy... OK (0.0000)
      → answer_similarity... ERREUR : AttributeError: 'OllamaRagasEmbeddings' object has no attribute 'run_config'


================================================================================
RÉSULTATS RAGAS
================================================================================

TEST 1
--------------------------------------------------------------------------------
Question : Quel joueur a le meilleur pourcentage à 3 points sur les 5 derniers matchs ?
Context Precision : 1.0000
Context Recall    : 1.0000
Faithfulness      : 1.0000
Response Relevancy: 0.8758
Answer Similarity : nan

TEST 2
--------------------------------------------------------------------------------
Question : Compare l'efficacité défensive de l'équipe à domicile et à l'extérieur.
Context Precision : 1.0000
Context Recall    : 1.0000
Faithfulness      : 1.0000
Response Relevancy: nan
Answer Similarity : nan

TEST 3
--------------------------------------------------------------------------------
Question : Combien de paniers le coach a-t-il marqués pendant le debrief du 12 mars ?
Context Precision : 0.0000
Context Recall    : 1.0000
Faithfulness      : 1.0000
Response Relevancy: 0.0000
Answer Similarity : nan


================================================================================
MOYENNES
================================================================================
context_precision      : 0.6667
context_recall         : 1.0000
faithfulness           : 1.0000
response_relevancy     : 0.4379
answer_similarity      : NaN
================================================================================

Résultats sauvegardés dans : ragas_results_ollama.json

Évaluation terminée.                                                          python .\eval_ragas_ollama2.py
^Cvenv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> 
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\eval_ragas_ollama.py 
C:\Users\nabil\AppData\Local\Programs\Python\Python312\python.exe: can't open file 'C:\\Users\\nabil\\Documents\\OC\\MLOPS\\Projet1\\P1_Code_Python\\P10_DSML\\eval_ragas_ollama.py': [Errno 2] No such file or directory
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\evaluate_ragas_ollama.py
Traceback (most recent call last):
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\evaluate_ragas_ollama.py", line 12, in <module>
    from langchain_ollama import ChatOllama, OllamaEmbeddings
ModuleNotFoundError: No module named 'langchain_ollama'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> uv add -U langchain-core
warning: `VIRTUAL_ENV=C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
Resolved 113 packages in 4.03s
Prepared 9 packages in 10.56s
Uninstalled 9 packages in 3.24s
Installed 9 packages in 1.76s
 - google-genai==2.27.0
 + google-genai==2.28.0
 - langchain-core==0.3.86
 + langchain-core==1.6.6
 - mcp==2.2.0
 + mcp==2.3.0
 - mcp-types==2.2.0
 + mcp-types==2.3.0
 - openai==3.23.0
 + openai==3.24.0
 - pydantic-ai==2.53.0
 + pydantic-ai==2.54.0
 - pydantic-ai-slim==2.53.0
 + pydantic-ai-slim==2.54.0
 - pydantic-evals==2.53.0
 + pydantic-evals==2.54.0
 - pydantic-graph==2.53.0
 + pydantic-graph==2.54.0
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\evaluate_ragas_ollama.py
Traceback (most recent call last):
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\evaluate_ragas_ollama.py", line 12, in <module>
    from langchain_ollama import ChatOllama, OllamaEmbeddings
ModuleNotFoundError: No module named 'langchain_ollama'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> Get-Content .\evaluate_ragas_ollama.py -TotalCount 20
import os
import logging

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv

from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_ollama import ChatOllama, OllamaEmbeddings

from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._answer_relevance import ResponseRelevancy
from ragas.metrics import _AnswerSimilarity

import logfire
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\evaluate_ragas_ollama.py                    
Traceback (most recent call last):
  File "C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\evaluate_ragas_ollama.py", line 12, in <module>
    from langchain_ollama import ChatOllama, OllamaEmbeddings
ModuleNotFoundError: No module named 'langchain_ollama'
(.venv) PS C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML> python .\evaluate_ragas_ollama.py

================================================================================
RAGAS 0.4.3 + OLLAMA
================================================================================

Configuration :
  Ollama      : http://localhost:11434
  LLM         : llama3.1:latest
  Embeddings  : nomic-embed-text:latest
  OpenAI      : NON
  Mistral     : NON
  LangChain Ollama : NON

================================================================================
TEST OLLAMA
================================================================================
URL Ollama       : http://localhost:11434
LLM              : llama3.1:latest
Embeddings       : nomic-embed-text:latest

[1/2] Test du LLM...
      ✓ LLM opérationnel
      Réponse : OLLAMA_LLM_OK

[2/2] Test des embeddings...
      ✓ Embeddings opérationnels
      Dimension du vecteur : 768

✓ Ollama est opérationnel.
C:\Users\nabil\Documents\OC\MLOPS\Projet1\P1_Code_Python\P10_DSML\evaluate_ragas_ollama.py:346: DeprecationWarning: Importing AnswerSimilarity from 'ragas.metrics' is deprecated and will be removed in v1.0. Please use 'ragas.metrics.collections' instead. Example: from ragas.metrics.collections import AnswerSimilarity
  from ragas.metrics import AnswerSimilarity

================================================================================
INITIALISATION RAGAS
================================================================================
LLM         : Ollama / llama3.1:latest
Embeddings  : Ollama / nomic-embed-text:latest

✓ Context Precision
✓ Context Recall
✓ Faithfulness
✓ Response Relevancy
✓ Answer Similarity

================================================================================
ÉVALUATION
================================================================================

TEST 1/3
Question : Quel joueur a le meilleur pourcentage à 3 points sur les 5 derniers matchs ?
  Context Precision... ✓ 1.0000
  Context Recall... ✓ 1.0000
  Faithfulness... ✓ 1.0000
  Response Relevancy... ✓ 0.8651
  Answer Similarity... ✗ ERREUR
      AttributeError: 'OllamaEmbeddings' object has no attribute 'run_config'

TEST 2/3
Question : Compare l'efficacité défensive de l'équipe à domicile et à l'extérieur.
  Context Precision... ✓ 1.0000
  Context Recall... ✓ 1.0000
  Faithfulness... ✓ 1.0000
  Response Relevancy... ✗ ERREUR
      OutputParserException: Invalid json output: Combien de points concède l\'équipe lorsqu\'elle joue à domicile?
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 
  Answer Similarity... ✗ ERREUR
      AttributeError: 'OllamaEmbeddings' object has no attribute 'run_config'

TEST 3/3
Question : Combien de paniers le coach a-t-il marqués pendant le debrief du 12 mars ?
  Context Precision... ✓ 0.0000
  Context Recall... ✓ 1.0000
  Faithfulness... ✓ 1.0000
  Response Relevancy... ✗ ERREUR
      OutputParserException: Invalid json output: The output string did not satisfy the constraints given in the prompt. Fix the output string and return it.
Please return the output in a JSON format that complies with the following schema as specified in JSON Schema:
{"properties": {"question": {"title": "Question", "type": "string"}, "noncommittal": {"title": "Noncommittal", "type": "integer"}}, "required": ["question", "noncommittal"], "title": "ResponseRelevanceOutput", "type": "object"}
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 
  Answer Similarity... ✗ ERREUR
      AttributeError: 'OllamaEmbeddings' object has no attribute 'run_config'

================================================================================
RÉSULTATS RAGAS
================================================================================

TEST 1
Question : Quel joueur a le meilleur pourcentage à 3 points sur les 5 derniers matchs ?
  Context Precision      : 1.0000
  Context Recall         : 1.0000
  Faithfulness           : 1.0000
  Response Relevancy     : 0.8651
  Answer Similarity      : NaN

TEST 2
Question : Compare l'efficacité défensive de l'équipe à domicile et à l'extérieur.
  Context Precision      : 1.0000
  Context Recall         : 1.0000
  Faithfulness           : 1.0000
  Response Relevancy     : NaN
  Answer Similarity      : NaN

TEST 3
Question : Combien de paniers le coach a-t-il marqués pendant le debrief du 12 mars ?
  Context Precision      : 0.0000
  Context Recall         : 1.0000
  Faithfulness           : 1.0000
  Response Relevancy     : NaN
  Answer Similarity      : NaN

================================================================================
MOYENNES
================================================================================
Context Precision      : 0.6667
Context Recall         : 1.0000
Faithfulness           : 1.0000
Response Relevancy     : 0.8651
Answer Similarity      : NaN
================================================================================

Résultats sauvegardés dans : ragas_results_ollama1.json

✓ Évaluation terminée.