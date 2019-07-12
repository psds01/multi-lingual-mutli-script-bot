Note: 
1. The terminologies used here are from "Rasa Space": component, slot, tracker, etc. Familiarity with Rasa is assumed.
2. Please review the **Note** at the end of this file!

## Motivation
Why I am doing this? Let's quote Rasa here:

*"The driver for our research is this: what would help developers build great conversational software? How can we enable them to build things that are currently out of reach? The primary outcome of our research is new features in the open source Rasa Stack."*

Let's see if we can build something that rasa currently doesn't support.

## Task : make a bot using Rasa that supports 
1. multiple languages
2. multiple scripts

In the project, we will demonstrate how to build a bot that
1. Understands multiple languages (in this case English and Hindi, "en" and "hi" henceforth resp.)
2. Detects scripts, here Devnagari and Latin, from the text message and 
3. Replies in the *script and language* found in the latest user message. This is just for fun, not a practical thing to do.

What novel thing is this project going to do?
1. How to write custom NLP components
2. How to add additional properties to `Message` object and drive conversations using them.
3. ~~How to make `rasa core` ignore these additional `Message` properties.~~
4. ~~Test the [`unfeaturized`](https://github.com/RasaHQ/rasa/issues/3754) slot type.~~
5. ~~Add as needed..~~

## Solution
### Overview of the solution

Let's zoom out a bit and try to see which part of Rasa Stack *drives* conversations: `core`. For a conversation to move ahead, which is governed by `core`, it doesn't matter which language/script was used by a user to send messages. Core is agnostic to the user's language/script. This implies we need to handle multiple languages *at* the `nlu` part of the Rasa Stack.

There are other ways in which this can be accomplished but we will train two different models : 
1. to detect language: so that we can reply in the same language
2. to detect language-agnostic intent: so that `core` can understand what the user is saying

The data for these two models looks like this:
```
## intent:hi_greet
 - namaste
 - kaise ho

## intent:greet
 - hi
 - hello
 - wassup!
```

The intents `hi_greet` and `greet` will be mapped to `greet` while training the component after stripping off the language info: `hi_` in `hi_greet`. If the intent starts with `hi` then it's in Hindi *language* else it's in English. This way we can annotate a text for two different kinds of labels: langauge and intent. This is (definitely?) hacky!


By doing so, we expect a single model to learn intents from different languages. This might not be ideal in practice and one might need to detect language and its intent using two diffferent models, but for simplicity, let's just stick with one model doing both the task. [#Explore: how far away can you take this approach? Where does this assumption break or is no more practical]

The script of text that was used also does not matter to the `core`. we will do script detection and its translation/transliteration at `nlu` of the Rasa Stack. This will not be done using any model though. We will use some package/library to transliterate the text and add it as property to the message. We will transliterate everything to Latin before classifying its intent.

Both language and script will be added to the message with `add_to_output=True` so that the `tracker` from `rasa_sdk` will get that info, which we will use to converse in the latest observed language with latest observed script.


## Custom Pipeline
Let's take a look at our `pipeline` of `component`s.

Pipeline overview:
```
custom_pipeline: 
    ScriptExtractor: text --> script
    LatinTextExtractor: text, script --> latin_text
    CustomFeaturizer: latin_text --> latin_text_features
    LanguageExtractor: latin_text_features --> language
    CustomIntentClassifier: latin_text_features --> intent

```

The (unwisely named) `custom_pipeline` has five components : each doing a specific task (A `pipeline` is like a `class` and a `component` is like a `function`! Rasa's design is so cool!)

1. script detector : it detects script from the raw text received from the user.
2. latin text extractor : it takes text and script, and transliterates text into latin_text if script is devanagari
3. custom featurizer : makes bigrams and skip-grams out of latin_text to give latin_text_features
4. language extractor : this is actually a classifier, I have misplaced it into `../extractors/`. Anyway, gets language from latin_text_features
5. custom intent classifier : this gives us language-agnostic intent from latin_text_features

You can find all about this custom pipeline here : [rasa_custom](https://github.com/psds01/rasa_custom)

## Installations
1. Install this first: rasa x
2. **IMPORTANT**: Then replace `rasa` from `site-packages` with this: https://github.com/psds01/rasa_custom
3. Then install this: https://pypi.org/project/indic-transliteration/


## Training the bot

Here, we will train the [rasa init](https://rasa.com/docs/rasa/user-guide/rasa-tutorial/) bot with the same stories but with different data which you can find in `/data/nlu.md`

The template for `utter_cheer_up` will also be changed to support language and script since it contains an image. 

Train the bot with 
```
rasa train
```

## Actions
The default rasa init bot does not come with custom actions. **Let's create custom actions that will reply in language and script that was used in the latest user message.**

For me, `Language` is what you'd hear if you read that text out loud and `Script` is what you'd see!

So, `namaste` is in `Hindi` language with `Latin` script and `हेल्लो` is in English language in Devanagari Script.

Check:
1. `actions.py` for actions and how it gets language and script from latest user message
2. `action_utterance_templates.py` for utterance templates of each action in Hindi and English language and in Devanagari and Latin script.

## Run the bot
Now since we have custom actions as well, run actions server:
```
python -m rasa_sdk --actions actions
```
Now run rasa bot with
```
rasa x
```

## Demo

Check out the `./screenshots/` folder


#### It's the crucial that you replace contents of your `rasa` package from `site-packages` with contents of [`rasa_custom`](https://github.com/psds01/rasa_custom) otherwise this pipeline will not work!!