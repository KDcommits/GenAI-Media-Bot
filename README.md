<h2 align="center"> GenAI-Media-Bot </h2>

<h3>Problem Statement:</h3>
Create a chatbot powered by Generative AI to:<br>
  1. Query SQL database and fetch user accurate answer even for the smallest of granular ask.<br>
  2. Query a pdf document and must reference the page number while answering the user's question. <br>
  3. Must support textual and audio-based questions. <br>

<h3>Approach:</h3>
`1. SQL-Level Query:`<br>
      1. Set-up a connection with mysql database with mysql-connector.<br>
      2. Fetch the database schema information under consideration and pass it as the context of the LLM.<br>
      3. Use OpenAI's GPT-3.5-Turbo-0613 Model and leverage it's function calling attrbute to do the magic. <br>

      
![image](https://github.com/KDcommits/GenAI-Media-Bot/assets/124420761/f8a61c9a-7236-4c3b-81a9-de6cee4971f3)

