# A few notes from my quick work

## User Features

we're missing the user features to adjust by user skill level. This is something simple we'll pass to the LLM that changes the context we give it. We need to add a user table in our db to support this.

user uuid
user name
user password // should be encrypted
user skill_level

## LLM Interactions

We're missing logging for LLM interactions. This was underlined as a critical feature in our progress report for safety testing and verification. I'll need to add a table for this as well, and we'll need some backend support.

user uuid
session id
timestamp
llm input // could reference source data from other tables
llm response

## Time Allocations

Since it's python, I can probably knock it out this afternoon. We need to put together ppts for our presentation, and the report itself before wednesday. the ppt slides can probably come from the report, so getting a draft of that put together should come first.

## Moving Forward

1. Database Finish this afternoon
    - Optinally: Help with back-end
2. Report tonight/tomorrow morning
3. 4 Slides **MAX**, done by Monday meeting
4. Monday Meeting afternoon 2-3
