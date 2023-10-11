<h2 align="center"> GenAI-Media-Bot </h2>

<h3>Problem Statement:</h3>
Create a chatbot powered by Generative AI to:<br>
  1. Query SQL database and fetch user accurate answer even for the smallest of granular ask.<br>
  2. Query a pdf document and must reference the page number while answering the user's question. <br>
  3. Must support textual and audio-based questions. <br>

<h3>Approach:</h3>
A.  SQL-Level Query:<br>
    - Set-up a connection with mysql database with mysql-connector.<br>
    - Fetch the database schema information under consideration and pass it as the context of the LLM.<br>
    - Use OpenAI's GPT-3.5-Turbo-0613 Model and leverage it's function calling attrbute to write the SQL query. <br>
    - Use the SQL query to derive the result from the database.<br><br>
B.  PDF-Level Query:<br>
    - Temporarily store the pdf uploaded by the user untill the page gets refreshed.<br>
    - Extract text out of the pdf and create overlapping text chunks of desirable lengths.<br>
    - Use an embedding model to create vector embeddings of those chunks.<br>
    - Store the embedding vector unto a in-memory vector database that gets deleted everytime user session is refreshed.<br>
    - Fetch top k chunk having most similarity with the embedded vector of user's question.<br>
    - Pass the content of the top k chunk as the context of the GPT-3.5-Turbo Model of OpenAI.<br>
    - Let the LLM use it's power to generate the answer with the most human readable format.<br><br>

      
![image](https://github.com/KDcommits/GenAI-Media-Bot/assets/124420761/f8a61c9a-7236-4c3b-81a9-de6cee4971f3)

