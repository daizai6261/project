import requests
import json

def chat(prompt="What is the point of life?", 
         systemMessage="你是一个人工智能助手，请遵循用户的指令，满足用户需求，用 Markdown 格式回复。",
         temperature=0.8, 
         top_p=1,
         model="gpt-3.5",
         channel="changan",
         max_retries=3,
        ):
    """
    Send a prompt to the specified chat API and return the chat response.

    Parameters:
    - prompt: The question or statement you want to send to the chatbot.
    - systemMessage: System message to be sent.
    - temperature: Controls randomness of the chatbot's replies. Higher values make it more random.
    - top_p: Controls diversity of chatbot replies. A value of 1 allows any token to be used in replies, while values <1 limit the selection.
    - model: The model to use for the chatbot (either "gpt-3.5" or "gpt-4").

    Returns:
    The chatbot's response text.
    """
    
    if channel == "changan":
        api_key = "02df0b280315480e87a0b12ac2812d3f"
        # api_key = "37a51b17ba51409191af3ccbd372e2fd"
        
        if model == "gpt-3.5":  # changan only has gpt-3.5
            model_name = "CHANGAN-GPT35-TURBO-16K"
            # url = "http://119.91.201.17:5000/send_message"
            url = "https://changan-chatgpt-test.openai.azure.com/openai/deployments/CHANGAN-GPT35-TURBO-16K/chat/completions?api-version=2023-05-15"
        else:
            raise Exception("channel 'changan' only supports model 'gpt-3.5'")

        headers = {
            "api-key": api_key,
        }

        # Define the POST request body
        body = {
            "messages": [
                {
                    "role": "system",
                    "content": systemMessage
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "top_p": top_p
        }
        
        tries_count = 0
        while True:
            tries_count += 1
            try:
                if tries_count > max_retries:
                    print("Max retries exceeded. Aborting.")
                    break
                # Send the POST request
                response = requests.post(url, headers=headers, json=body)

                # Check if the request was successful
                response.raise_for_status()

                # Extract and return the chatbot's reply from the response
                if "send_message" in url:
                    ret = response.json()["answer"]
                else:
                    ret = response.json()["choices"][0]["message"]["content"]
                return ret
            except Exception as e:
                print(e)
                print(response.json())
                print("Retrying... channel:", channel,"model_name:", model_name)
    else:
        # Define the API endpoint based on the selected model
        from openai import OpenAI

        client = OpenAI(
            # 使用你的实际 API 密钥
            # api_key="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",   # 厦门账号
            # api_key="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",   # 我自己的
        )
        
        tries_count = 0
        while True:
            tries_count += 1
            if tries_count > max_retries:
                print("Max retries exceeded. Aborting.")
                break
            if model == "gpt-4":
                model_name = "gpt-4-1106-preview"
            else:
                model_name = "gpt-3.5-turbo-1106"
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    # response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": systemMessage},
                        {"role": "user", "content": prompt}
                    ]
                )
                ret = response.choices[0].message.content
                return ret
            except Exception as e:
                print(e)
                print("Retrying... channel:", channel, "model_name:", model_name)
    return None


# Test the function
if __name__ == "__main__":
    response_text = chat(
        prompt="你好！你是谁？",
        model="gpt-3.5",
        channel="americancenter",
        )
    # response_text = chat(model="gpt-4")
    print(response_text)
