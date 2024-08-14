from global_search import ask_query_global
from local_search import ask_query_local

print("===================Global Search===================")
res = ask_query_global('''Search for grants based on the following requirements: grant_amount=250000 USD 
eligibility_criteria=['Foreign National'] 
grant_category=Business 
project_name=Alpha Dating App 
project_description=Connect straight people with like-minded individuals for dating and marriage assistance, including wedding planning services. 
project_usecase=Primary use case is to connect straight individuals for dating and offer comprehensive wedding planning services. Additionally, an Advisory Council will help couples with pre-marriage compatibility checks and ongoing marital support. 
project_outcomes=Increased marriage rates and decreased divorce rates.
project_execution_plan=1-year development phase, 6 months of beta testing, and then public release of the product.
                       
Write a sample Grant Drafts for all the requirements mentioned above for me to submit a grant.
''')
print(res)
print('==================================================')
print(res['response'])

print("===================Local Search===================")
res = ask_query_local('''Search for grants based on the following requirements: grant_amount=250000 USD 
eligibility_criteria=['Foreign National'] 
grant_category=Business 
project_name=Alpha Dating App 
project_description=Connect straight people with like-minded individuals for dating and marriage assistance, including wedding planning services. 
project_usecase=Primary use case is to connect straight individuals for dating and offer comprehensive wedding planning services. Additionally, an Advisory Council will help couples with pre-marriage compatibility checks and ongoing marital support. 
project_outcomes=Increased marriage rates and decreased divorce rates.
project_execution_plan=1-year development phase, 6 months of beta testing, and then public release of the product.

Write a sample Grant Drafts for all the requirements mentioned above for me to submit a grant.
''')
print(res)
print('==================================================')
print(res['response'])