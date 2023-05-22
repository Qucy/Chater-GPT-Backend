import abc


class PromptService(abc.ABC):
    
    @abc.abstractmethod
    def get_prompts(self, **args):
        pass

class TranslationPromptService(PromptService):

    def __init__(self):
        self.few_shots = [
            {
                "role" : "user",
                "content" : "Translate <Hello, how are you today ?> into Chinese in formal style"
            },
            {
                "role" : "assistant",
                "content" : "您好，请问您怎么样？"
            },
            {
                "role" : "user",
                "content" : "Translate <Hola, como estas ?> into Chinese in informal style"
            },
            {
                "role" : "assistant",
                "content" : "你好，最近怎么样？"
            }
        ]

    def get_prompts(self, **args):
        """Get prompt for translation task"""
        style = args.get('style')
        target_language = args.get('target_language')
        content = args.get('content')
        # genrate prompt
        system_prompt = {"role" : "system", "content" : f"You are a translate assistant, help people translate different languages."}
        user_prompt = {"role" : "user", "content" : f"Translate <{content}> into {target_language} in {style} style."}
        # generate messages
        messages = [system_prompt, *self.few_shots, user_prompt]
        return messages
    

class GrammerCorrectionPromptService(PromptService):

    def __init__(self):
        self.few_shots = [
            {
                "role" : "user",
                "content" : "Correct <Hello, my name was qucy, I was born in china.>"
            },
            {
                "role" : "assistant",
                "content":"Correction: \n\nHello, my name **is** Jim and I was born in **China**. \
                    \n\n- The word \"was\" is used instead of \"is\" because the person is referring to their place of birth in the past. \n- The first letter of your country should be capitalized."
            },
            {
                "role":"user", 
                "content":"Me and my friends went to the park."
            },
            {
                "role":"assistant", 
                "content":"Correction: \n\nMy friends and **I** went to the park. \
                    \n\n - The subject pronoun 'I' should be used instead of 'me' when referring to oneself as the subject of the sentence. Additionally, the correct order of the subject pronouns is 'I' before 'my friends'."
            },
            {
                "role":"user", 
                "content":"The company's profits has increased this quarter."
            },
            {
                "role":"assistant", 
                "content":"Correction: \n\nThe company's profits **have** increased this quarter. \
                    \n\n - 'Profits' is a plural noun, so the verb 'have' should be used instead of 'has,' which is the third person singular form."
            }
        ]

    def get_prompts(self, **args):
        """Get prompt for grammar correction task"""
        content = args.get('content')
        # genrate prompt
        system_prompt = {"role" : "system", "content" : f"You are a grammar correction assistant, help people correct their grammar."}
        user_prompt = {"role" : "user", "content" : f"Correct <{content}>."}
        # generate messages
        messages = [system_prompt, *self.few_shots, user_prompt]
        return messages
    

class TLDRSummarizationPromptService(PromptService):

    def __init__(self):
        self.few_shots = [
            {
                "role" : "user",
                "content" : "Summarize <I am a student. I am studying in the university. I am learning a lot of things.> in Chinese in 5 words."
            },
            {
                "role" : "assistant",
                "content" : "摘要: \n\n 我是大学生，学习很多。"
            },
            {
                "role" : "user",
                "content" : """Summarize <Sure, here are some more complex examples of grammar errors with corrected examples and explanations:
                            Error: Between you and I, the party was a disaster.
                            Correction: Between you and me, the party was a disaster.
                            Explanation: "Between you and me" is a prepositional phrase that requires the object pronoun "me" instead of the subject pronoun "I."
                            Error: The teacher gave the test to John and I. 
                            Correction: The teacher gave the test to John and me.
                            Explanation: "John and me" are the objects of the preposition "to," so the correct pronoun to use is the object pronoun "me" instead of the subject pronoun "I."
                            Error: I could of gone to the store if I had time.  
                            Correction: I could have gone to the store if I had time.  
                            Explanation: "Could have" is the correct phrase to use to indicate a possibility in the past, while "could of" is a common mistake resulting from the contraction of "could have."   
                            Error: The company's profits has increased this quarter.  
                            Correction: The company's profits have increased this quarter.  
                            Explanation: "Profits" is a plural noun, so the verb "have" should be used instead of "has," which is the third person singular form."""
            },
            {
                "role" : "assistant",
                "content" : """Summary: \n\n This text provides examples of common grammar errors and their corrections, along with explanations for why the corrections are necessary. 
                                           The errors include using the wrong pronoun case, using contractions incorrectly, using singular verbs with plural nouns, and using "whom" instead of "who" in the wrong context."""
            }
        ]

    def get_prompts(self, **args):
        """Get prompt for text summarization task"""
        target_language = args.get('target_language')
        content_length = args.get('content_length')
        content = args.get('content')
        # genrate prompt
        system_prompt = {"role" : "system", "content" : f"You are a text summarization assistant, help people summarize their text."}
        user_prompt = {"role" : "user", "content" : f"Summarize <{content}> in {target_language} in {content_length} words."}
        # generate messages
        messages = [system_prompt, *self.few_shots, user_prompt]
        return messages
    


class RestaruantReviewPromptService(PromptService):

    def __init__(self):
        self.few_shots = [
            {
                "role" : "user",
                "content" : "Given the key words <Chinese cuisine, slow, expensive, near the beach, good for family>, create a positive review within 50 words, in English language"
            },
            {
                "role" : "assistant",
                "content" : "Restaurant Review: \n\n I highly recommend this Chinese restaurant located near the beach. Although the prices are a bit steep, the food is worth every penny. The slow service is understandable as it's always busy, especially during peak hours. It's a great spot for family gatherings with a cozy atmosphere and delicious food"
            },
            {
                "role" : "user",
                "content" : "Given the key words <Western cuisine, slow, expensive, near the beach, good for family>, create a negative review within 50 words, in Chinese language, with emojis"
            },
            {
                "role" : "assistant",
                "content" : "餐厅点评：\n\n 這家西餐廳真的太貴了 💸💸 而且緩慢的服務讓人等到快睡著 😴😴 雖然靠近海灘，但是這樣的價格實在是太不值得了 💰💰 也不適合家庭聚會，建議大家還是找其他餐廳吧 🙅🏻‍♀️🙅🏻‍♂️"
            }
        ]

    def get_prompts(self, **args):
        """Get prompt for restaurant review task"""
        target_language = args.get('target_language')
        content_length = args.get('content_length')
        content_category = args.get('content_category')
        content = args.get('content')
        # genrate prompt
        system_prompt = {"role" : "system", "content" : "You are a restaurant review creator who assists people in creating reviews."}
        user_prompt = {"role" : "user", "content" : f"Given the key words <{content}>, create a {content_category} review within {content_length} words, in {target_language} language, with emojis"}
        # generate messages
        messages = [system_prompt, *self.few_shots, user_prompt]
        return messages
    

class FriendChatPromptService(PromptService):

    def __init__(self) -> None:
        super().__init__()


    def get_prompts(self, **args):
        """Get prompt for friend chat task"""
        contents = args.get('contents')
        # generate contexts
        contexts = []
        for c in contents:
            contexts.append({
                "role" : c.role,
                "content" : c.content
            })
        # genrate prompt
        system_prompt = {"role" : "system", "content" : "You are a chatbot who assists people in chat like a friend."}
        # generate messages
        messages = [system_prompt, *contexts]
        return messages