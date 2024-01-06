import openai
import pandas as pd
import json
from openai import AsyncOpenAI
openai.api_key = "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"


def get_prompt():
    return ''' Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.
    Then retrieve a stock symbol corresponding to that company. For this you can use 
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this,
    {

        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": 12.34 million",
        "Net Income" : 34.78 million",
        "EPS": "2.1 $"

    }

    News Article:
    ==============


    '''
def extract_financial_info(text):
    prompt = get_prompt() + text
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{'role':'user','content':prompt}]

    )


    content = response.choices[0]['message']['content']

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(),columns = ["Measure","Value"])

    except (json.JSONDecodeError,IndexError):
        pass

    return pd.DataFrame({
        "Measure" : ["Company Name","Stock Symbol","Revenue","Net Income","EPS"],
        "Value": ["","","","",""]
    })
    return content


if __name__ == "__main__":
    text = '''
    
    Tesla's Earning news in text format : 
    Tesla's earning this quarter
    
    '''
    data = extract_financial_info(text)