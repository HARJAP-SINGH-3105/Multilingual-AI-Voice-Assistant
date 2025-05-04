import requests
import json
import os
from crewai.tools import tool
from crewai import Agent
from crewai import Task, Crew, Process
from dotenv import load_dotenv
from crewai import LLM
load_dotenv()



def solve_query(question):


    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    gemini_api_key =  os.getenv('GOOGLE_API_KEY')

    @tool("web_search")
    def web_search_tool(query:str)->str:
        """
        Performs a Google search using the Serper.dev API and returns structured results.

        Parameters:
        -----------
        query : str
            The search query string to look up on Google.
        Returns:
        --------
        str
            A formatted string containing extracted fields from the search results,
            including 'searchParameters', 'answerBox', 'knowledgeGraph', and 'organic',
            if present in the API response.

        Notes:
        ------
        - The request is sent to the Serper.dev `/search` endpoint with `gl='in'` to simulate results from India.
        - The function currently processes and includes only selected parts of the JSON response.
        - The output is intended to be human-readable, with each section clearly labeled and separated.
        """

        # query = inputs.get("query")
        # if not query:
        #     return "Error: 'query' parameter is missing."
        
        url = "https://google.serper.dev/search"
        serpdev_api = os.getenv('SERPDEV_API_KEY')
        payload = json.dumps({
            "q": query,
            "gl": "in",  # Location: India
            "num": 2 # Took top 5 organic results only
        })
        headers = {
            'X-API-KEY': serpdev_api,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_reply = json.loads(response.text)
        # return json_reply
        req_info = ['searchParameters', 'answerBox', 'knowledgeGraph','organic']
        
        final_res = ''
        for item in req_info:
            if item in json_reply:
                final_res += item + ' :\n'
                final_res += str(json_reply[item]) 
                final_res += '\n-----------------------------------------------------------------------------------\n\n'

        return final_res


    llm = LLM(
        model="gemini/gemini-2.0-flash",
        provider="google_gemini",                     # ✅ use Gemini via API Ke # ✅ put your key directly
        api_key= gemini_api_key,
        temperature=0.5
    )


    search_agent = Agent(
        role="Search Specialist",
        goal=" Search the internet for real-time, relevant and factual information about any user query. ",
        tools=[web_search_tool],
        llm =llm,
        backstory="Expert in extracting and summarizing real-time info using web tools",
        # verbose =True,
        allow_delegation=False,
        max_iter =1
    )

    answer_agent = Agent(
        role="User query solver",
        goal="Use the researched web content to understand and produce a summarized, high-quality answer",
        tools =[],
        llm= llm , # you can wrap Gemini via an LLM wrapper or use your own function
        api_key = gemini_api_key,
        backstory="Specializes in analyzing content and summarizing insights in a human-understandable format.",
        # verbose= True,
        allow_delegation=False,
        max_iter =1
    )



    search_task = Task(
        agent=search_agent,
        description=(  
            "Use the `web_search` tool to research the latest and most relevant information from the web "
            "for the user's question: '{query}'. Return a structured context summary. "),
        expected_output="A compiled context summary based on search results from web."
    )

    answer_task = Task(
        agent=answer_agent,
        description="Use the provided context and take the help of web-search to generate a final answer about given user query:\n {query}",
        expected_output="A human-like answer addressing the user query based on the context and web-search."
    )

    crew = Crew(
        tasks=[ search_task,answer_task],
        agents=[search_agent, answer_agent],
        # verbose = True,
        cache=False,
        process=Process.sequential, 
    )

    result = crew.kickoff(inputs={'query': question})

    return result

