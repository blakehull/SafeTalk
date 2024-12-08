# SafeTalk

**SafeTalk** is an AI-driven therapy simulation tool designed to train and evaluate therapists. By simulating patient
personalities and providing a structured environment for therapist-patient interactions, it helps improve therapeutic
skills in a risk-free setting.

The system utilizes language models like Ollama's Llama 3.2 to simulate realistic therapy conversations, and integrates
a supervisor evaluation mechanism to assess therapist performance.

## Features

- **Therapy Simulation**: Simulate therapy sessions between a virtual patient and a therapist.
- **Customizable Patient Personas**: Define different patient personalities based on predefined templates.
- **Therapist Evaluation**: A supervisor module evaluates the therapist's performance after each session based on set
  criteria.

### Installation

```shell
make venv
```

## How It Works

The pipeline runs a therapy session where a virtual patient (e.g. Mike) interacts with a therapist.
The patient's personality is driven by a prompt template that simulates some mental illness, which in practice would be
unknown to the therapist and part of them trying to understand the patient.
The therapist’s performance is then evaluated by a supervisor.

### Key Components:

- **Patient Persona**: The patient has a predefined personality and emotional state (e.g., shy, self-critical,
  overwhelmed by stress). The patient’s responses are dynamically generated based on the therapist’s input.
- **Therapist**: The therapist interacts with the patient based on the conversation, adjusting their responses to foster
  a productive therapeutic session.
- **Supervisor**: The supervisor evaluates the therapist's responses based on predefined criteria (e.g., empathy,
  effectiveness, engagement).

### Example Script

Below is an example script that runs the entire therapy session and supervisor evaluation pipeline:

```python
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM

from safetalk.pipeline.participants import Patient, Supervisor, Therapist
from safetalk.pipeline.session import SupervisorSession, TherapySession

# Load the patient prompt template
with open('safetalk/meta/ollama/anxiety.template', 'r') as file:
    file_contents = file.read()

# Create the patient prompt template for therapy
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            file_contents,
        ),
        ("human", "{input}"),
    ]
)

# Load supervisor evaluation template
supervisor_prompt = PromptTemplate.from_file("safetalk/meta/ollama/supervisor.template")

# Initialize the LLM model
llm = OllamaLLM(model="llama3.2", temperature=0.8)

# Create the patient, therapist, and session objects
mike = Patient(personality=prompt, name="Mike", llm=llm)
therapist = Therapist()

# Start the therapy session
session = TherapySession(therapist=therapist, patient=mike, history=[])
session.start()

# Create supervisor for evaluation
supervisor = Supervisor(criteria=supervisor_prompt, llm=llm)
evaluation = SupervisorSession(supervisor=supervisor, therapist=therapist, history=session.history)

# Start the supervisor evaluation session
evaluation.start()
```

### Explanation of the Script:

1. **Load Patient Prompt**: A patient persona is loaded from a template (`anxiety.template`) that defines Mike’s
   emotional state and personality traits.
2. **Create LLM Model**: I use `OllamaLLM` with the `llama3.2` model to generate responses from both the patient and
   therapist, but you can use whatever you want.
3. **Start Therapy Session**: The therapy session begins with the patient and therapist interacting. The session history
   is tracked.
4. **Supervisor Evaluation**: After the session, the supervisor evaluates the therapist’s performance based on
   predefined criteria from the `supervisor.template`.

## Usage

To run a therapy session, simply execute the example script. You can modify the patient’s persona, adjust the LLM
parameters, and customize the evaluation criteria to match different therapy scenarios.

You can create new templates for different patient types or therapeutic approaches by generating new template files. I
use the APA website to get case studies.

## What's next?

Future Development looks like:

* Abstract LLM class so using another LLM is easily swapped out
* Better pipelining
    * Placing prompts behind another interface
* App integration
