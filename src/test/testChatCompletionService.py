import unittest
from unittest import TestCase
from config.configuration import DevelopmentConfig
from service.chatCompletionService import AzureNormalChatCompletion, AzureStreamChatCompletion


class TestChatCompletionService(TestCase):

    def setUp(self) -> None:
        self.config = DevelopmentConfig()
        self.normal_completion = AzureNormalChatCompletion(self.config.api_deployment_name)
        self.stream_completion = AzureStreamChatCompletion(self.config.api_deployment_name)
        return super().setUp()
    

    def test_normal_completion(self):
        """test completion"""
        messages = [{"role": "user", "content": "Hello"}]
        response = self.normal_completion.completion(messages)
        print(response)
        self.assertIsNotNone(response)
        

    def test_stream_completion(self):
        """test stream completion"""
        response = self.stream_completion.completion([{"role": "user", "content": "Hello"}])
        for msg in response:
            print(msg)
            self.assertIsNotNone(msg)


if __name__ == '__main__':
    unittest.main()