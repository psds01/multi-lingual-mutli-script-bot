## happy path
* greet
  - action_greet
* mood_great
  - action_happy

## sad path 1
* greet
  - action_greet
* mood_unhappy
  - action_cheer_up
  - action_did_that_help
* affirm
  - action_happy

## sad path 2
* greet
  - action_greet
* mood_unhappy
  - action_cheer_up
  - action_did_that_help
* deny
  - action_goodbye

## say goodbye
* goodbye
  - action_goodbye
