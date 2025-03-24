from langchain_openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TextCleaningAgent:
    def __init__(self, api_key = OPENAI_API_KEY, chunk_size=2000, chunk_overlap=200):
        self.llm = OpenAI(api_key=api_key, temperature=0.1)  # Low temperature for consistency
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        self.cleaning_prompt = PromptTemplate(
            input_variables=["text_chunk"],
            template="""
            Clean and format the following text while preserving ALL information and details.
            Rules:
            1. Fix grammatical errors and typos
            2. Improve formatting and readability, also no need for URLs, width/height, and stuff which are not relevant to the content
            3. DO NOT remove any information
            4. DO NOT add new information
            5. Maintain the original meaning and context
            6. Keep the original text as much as possible
            7. When you process posts, keep the original post as much as possible, so that we can still have the original post readable, use a structure for it
            
            Important format:
            <profile information>
            <profile posts>
            <current company posts>
            
            Text to clean:
            {text_chunk}

            Cleaned text:
            <profile_information>
            {profile_information}
            </profile_information>
            
            <profile_posts>
            {profile_posts}
            </profile_posts>
            
            <company_posts>
            {company_posts}
            </company_posts>
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.cleaning_prompt)
    
    def clean_text(self, input_file_path, output_file_path):
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            raise Exception(f"Input file not found: {input_file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
        
        # Split text into manageable chunks
        chunks = self.text_splitter.split_text(text)
        
        # Process each chunk
        cleaned_chunks = []
        for chunk in chunks:
            cleaned_chunk = self.chain.run(text_chunk=chunk)
            cleaned_chunks.append(cleaned_chunk)
        
        # Combine cleaned chunks
        final_text = '\n'.join(cleaned_chunks)
        
        # Save the cleaned text
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(final_text)
        
        return final_text
