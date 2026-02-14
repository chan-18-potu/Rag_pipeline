from online_pipeline import answer_question

user_id = "<your_user_id_here>"
question = "What causes piston issues?"

answer, source = answer_question(user_id, question)

print("Answer:", answer)
print("Source:", source)
