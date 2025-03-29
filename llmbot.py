from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import Langchain and Hugging Face components
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Bot configuration
TOKEN: Final = '8142158412:AAEVhy1H_X2ZxT2wEqun_OxqD7SKWqnFqPo'
BOT_USERNAME: Final = 'wanderwbot'

# Initialize the LLM
def initialize_llm():
    print("Initializing LLM...")
    # Choose a smaller model that can run on CPU
    # You can change this to a larger model if you have GPU
    model_id = "distilgpt2"  # A lightweight model for demonstration
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=100,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    
    # Create a prompt template for travel assistance
    template = """
    You are a helpful travel assistant named WanderWBot.
    
    User question: {question}
    
    Please provide a helpful, friendly, and concise response:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["question"])
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain

# Initialize the LLM chain
llm_chain = initialize_llm()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am WanderWBot, your personal travel assistant powered by AI. How can I help you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'I am here to help you with your travel needs. You can ask me about:\n'
        '- Travel destinations\n'
        '- Packing tips\n'
        '- Local customs\n'
        '- Weather conditions\n'
        '- And more!\n\n'
        'Just type your question and I\'ll do my best to assist you.'
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.')

# Get response from LLM
def get_llm_response(text: str) -> str:
    try:
        # Use the LLM chain to generate a response
        response = llm_chain.run(question=text)
        return response.strip()
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "I'm having trouble processing that right now. Could you try again with a different question?"

# Fallback responses for when LLM fails or for simple queries
def get_fallback_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed or 'hi' in processed:
        return 'Hello there! How can I help with your travel plans today?'
    
    if 'how are you' in processed:
        return "I'm doing great, thanks for asking! Ready to assist with your travel queries."
    
    if 'thank' in processed:
        return "You're welcome! Feel free to ask if you need any more travel advice."
    
    return "I'm not sure I understand. Could you rephrase your question about travel?"

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
        
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User: {update.message.chat.id} Message Type: {message_type}')
    print(f'Message text: {text}')
    
    # Determine if we should process this message
    should_process = False
    processed_text = text
    
    if message_type == 'PRIVATE':
        should_process = True
    elif message_type == 'GROUP' or message_type == 'SUPERGROUP':
        if f'@{BOT_USERNAME}' in text:
            processed_text = text.replace(f'@{BOT_USERNAME}', '').strip()
            should_process = True
    
    if should_process:
        # Send typing action to show the bot is "thinking"
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        
        # Get response from LLM
        response = get_llm_response(processed_text)
        
        # If LLM fails or returns empty, use fallback
        if not response or len(response) < 5:
            response = get_fallback_response(processed_text)
        
        print(f'Bot: {response}')
        await update.message.reply_text(response)

async def error_handler(update, context):
    print(f'Update {update} Error: {context.error}')
    
if __name__ == '__main__':
    print("Bot is starting")
    
    # Build and configure the application
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    print("Bot is running with LLM integration")
    app.run_polling(poll_interval=3)
