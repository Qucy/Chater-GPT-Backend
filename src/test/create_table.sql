-- create a sqlite table called prompt_template with the following columns:
-- id, name, description, system_prompt, user_prompt, few_shots, created_at, updated_at
create table prompt_template (
    id integer primary key autoincrement,
    name text not null,
    description text not null,
    system_prompt text not null,
    user_prompt text not null,
    few_shots text not null,
    created_at datetime not null,
    updated_at datetime not null
);


-- create some dummy data for the prompt_template table
insert into prompt_template (name, description, system_prompt, user_prompt, few_shots, created_at, updated_at) values 
(
 'Summarization', 
 'Prompt template for summarization', 
 '{"system": "I want you to be a summerization bot"}', 
 '{Summarize <{content}> in {target_language} in {content_length} words.}', 
 '[
   {
     "role" : "user",
     "content" : "Summarize <I am a student. I am studying in the university. I am learning a lot of things.> in Chinese in 5 words."
   },
   {
     "role" : "assistant",
     "content" : "摘要: \n\n 我是大学生，学习很多。"
   }
  ]', 
  datetime('now'), 
  datetime('now')
);
insert into prompt_template (name, description, system_prompt, user_prompt, few_shots, created_at, updated_at) values 
(
 'Translation', 
 'Prompt template for translation', 
 '{"system": "I want you to be a translation bot"}', 
 '{Translate <{content}> from {source_language} to {target_language}.}', 
 '[
   {
     "role" : "user",
     "content" : "Translate <I am a student. I am studying in the university. I am learning a lot of things.> from English to Chinese."
   },
   {
     "role" : "assistant",
     "content" : "翻译: \n\n 我是大学生，学习很多。"
   }
  ]', 
  datetime('now'), 
  datetime('now')
);
insert into prompt_template (name, description, system_prompt, user_prompt, few_shots, created_at, updated_at) values 
(
 'Question Answering', 
 'Prompt template for question answering', 
 '{"system": "I want you to be a question answering bot"}', 
 '{Answer the question <{question}> in {target_language}.}', 
 '[
   {
     "role" : "user",
     "content" : "Answer the question <What is your name?> in Chinese."
   },
   {
     "role" : "assistant",
     "content" : "回答: \n\n 我的名字是小明。"
   }
  ]', 
  datetime('now'), 
  datetime('now')
);