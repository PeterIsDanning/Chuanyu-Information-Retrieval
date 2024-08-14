import ollama

def summary_generator(model, url):
    response = ollama.chat(model=model, messages=[
    {'role': 'user',
     'content': f'阅读网页({url})生成中文的总结',}])
    return response["message"]["content"]