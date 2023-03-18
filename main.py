import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def input_prompt(prompt: str):
    '''
    Tell EdgeGPT the prompt

    Args:
    - prompt (str)

    Returns:
    - result
    '''
    bot = Chatbot(cookiePath='./cookie.json')
    result = await bot.ask(prompt="Hi how are you doing?", conversation_style=ConversationStyle.creative)
    await bot.close()

    return result

if __name__ == "__main__":
    asyncio.run(main())