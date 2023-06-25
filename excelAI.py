import json
import pandas as pd 
import matplotlib.pyplot as plt  
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent 

class ExcelQuery:
    def __init__(self,OPENAI_KEY):
        self.OPENAI_KEY = OPENAI_KEY

    def _createPrompt(self, question):
        prompt = (
        """
        Let's decode the way to respond to the query asked within the delimiter #. The responses depend on the type of information requested in the query.

        1. If the query requires a table, format your answer like this:
           {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

        2. For a bar chart, respond like this:
           {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        3. If a line chart is more appropriate, your reply should look like this:
           {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        Note: We only accommodate two types of charts: "bar" and "line".

        4. For a plain question that doesn't need a chart or table, your response should be:
           {"answer": "Your answer goes here"}

        For example:
           {"answer": "The Product with the highest Orders is '15143Exfo'"}

        5. If the answer is not known or available, respond with:
           {"answer": "I do not know."}

        Return all output as a string. Remember to encase all strings in the "columns" list and data list in double quotes.
        For example: {"columns": ["Products", "Orders"], "data": [["51993Masc", 191], ["49631Foun", 152]]}

        Now, let's tackle the query step by step. Here's the query for you to work on:
        """
        + '#'+ question +'#'
    )

        return prompt
    
    def _create_plot(self,response_dict: dict):

        # Check if the response is an answer.
        if "answer" in response_dict:
            return response_dict["answer"]

        # Check if the response is a bar chart.
        if "bar" in response_dict:
            data = response_dict["bar"]
            try:
                plt.bar(data['columns'], data['data'])
                return plt.show()
            except ValueError:
                print(f"Couldn't create DataFrame from data: {data}")

        # Check if the response is a line chart.
        if "line" in response_dict:
            data = response_dict["line"]
            try:
                plt.line(data['columns'], data['data'])
                return plt.show()
            except ValueError:
                print(f"Couldn't create DataFrame from data: {data}")


        # Check if the response is a table.
        if "table" in response_dict:
            data = response_dict["table"]
            df = pd.DataFrame(data["data"], columns=data["columns"])
            return df


    def excelQuery(self,excel_filepath,question):
        df = pd.read_excel(excel_filepath)[:2]
        df_agent = create_pandas_dataframe_agent(OpenAI(model='text-davinci-002',openai_api_key = self.OPENAI_KEY, temperature =0), 
                                                        df, verbose =False,return_intermediate_steps=True)
        question_prompt = self._createPrompt(question)
        agent_response  = df_agent(question_prompt)
        final_thought  = agent_response['intermediate_steps'][-1][0].log.split('\n')[-1].split('Action Input:')[-1].strip()
        output_string = agent_response['output']
        output_dict = json.loads(output_string)
        return f"Answer : {output_dict['answer']} .\n\nQuery Used : {final_thought}"
    
        # if ('plot' in question) | ('draw' in question) | ('graph' in question) | ('chart' in question) | ('visualize' in question):
        #     return self._create_plot(output_dict)


    