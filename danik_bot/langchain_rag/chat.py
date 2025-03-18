import os
import pydotenv

from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer, PreTrainedTokenizerFast

env = pydotenv.Environment()

class ChatBot:
    def __init__(self, model_name: str = None, device: str = "cpu"):
        """
        Initialize the chatbot with the Hugging Face model and tokenizer.

        Args:
            model_name (str): Hugging Face model name or path.
            device (str): Device to use for inference ('cpu' or 'cuda').
        """
        model_name = env.get('CHAT_MODEL') if model_name is None else model_name
        self.device = device
        self.tokenizer: PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(model_name)
        self.model: OVModelForCausalLM = self._get_model(model_name)


    def _get_model(self, model_name):
        model_path = './models/mtsai'
        tokenizer: PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(model_name)
        model = OVModelForCausalLM.from_pretrained(model_name).to(self.device)
        if not os.path.exists(model_name):
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
        return model


    def generate_response(self, prompt: str, max_length: int = 150) -> str:
        """
        Generate a response to the given prompt using the loaded model.

        Args:
            prompt (str): The input text to the chatbot.
            max_length (int): Maximum length of the generated response.

        Returns:
            str: The chatbot's response.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        response_ = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response_.strip()


# Example usage (if you want to test this directly):
if __name__ == "__main__":
    bot = ChatBot()
    user_input = "Какие заведения стоит посетить с девушкой в Алматы?"
    response = bot.generate_response(user_input, max_length=300)
    print("Bot Response:", response)
