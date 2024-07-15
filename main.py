from assistant import *

mode = 2

if mode == 1: # create new assistant
    business_name = 'Ristorante Margheri'
    business_type = 'restaurant'
    business_place = 'Zurich, Switzerland'
    business_category = 'fine dining'
    instructions = f'''
                    You are a consultant for a {business_type}.
                    The restaurant is located in {business_place}.
                    They focus on {business_category}. Use your knowledge base to provide answers to the user's prompt.
                    '''

    assistant_id = create_new_assistant(business_name,instructions)
    thread_id = create_new_thread()
else:
    assistant_id = 'asst_RwNB1o5NOtUhDY64QBTpN0hG'
    thread_id = 'thread_UWE8HdzSOLp7CFbGwBrYDWIF'

## Update Knowledge Base
#file_paths = ["data/reviews.json", "data/reviews2.json"]
#assistant_id = update_assistant_with_files(assistant_id,file_paths)
run(assistant_id,thread_id)
