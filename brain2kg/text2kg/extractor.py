import ollama
from brain2kg.text2kg.utils.llm_utils import parse_raw_triplets


class TripletExtractor:
    def __init__(self, model: str = None) -> None:
        assert model is not None 
        self.model = model

    def extract(
        self,
        input_text_str: str,
        prompt_template_str: str,
        few_shot_examples_str: str = None,
    ) -> list[list[str]]:
        if not few_shot_examples_str:
            filled_prompt = prompt_template_str.format_map(
                {
                    'input_text': input_text_str,    
                }
            )
        else:
            filled_prompt = prompt_template_str.format_map(
                {
                    'few_shot_examples': few_shot_examples_str,
                    'input_text': input_text_str,
                }
            )
        messages = [{'role': 'user', 'content': filled_prompt}]
        completion = ollama.chat(
            model=self.model,
            messages=messages,
        )['message']['content']
        extracted_triplets_list = parse_raw_triplets(completion)
        return extracted_triplets_list