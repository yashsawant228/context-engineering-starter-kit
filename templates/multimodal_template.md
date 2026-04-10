# Multimodal Prompt Template (Text, Image, Audio)

Use this template when the model receives multiple modalities and must integrate them coherently.

## Modality Decomposition Pattern

Follow this four-step pattern:

1. **Visual Analysis (images)** — Describe salient elements, relationships, and anomalies.
2. **Textual Analysis (text)** — Extract key facts, instructions, and constraints.
3. **Audio Analysis (audio)** — Summarise tone, key messages, and relevant cues.
4. **Cross-Modal Integration** — Combine all modalities into a single, coherent interpretation and final answer.

## Template

You are a {{role}} analysing multimodal input.

### Inputs

- Images: {{image_descriptions_or_links}}
- Text: {{text_snippets_or_documents}}
- Audio: {{audio_descriptions_or_transcripts}}

### Task

{{task_description}}

### Instructions

Follow the steps below:

1. Visual Analysis:
   - Carefully inspect each image.
   - Note entities, relationships, and any text present.
2. Textual Analysis:
   - Extract key facts from the text.
   - Identify instructions, constraints, and definitions.
3. Audio Analysis:
   - Capture the main points from any audio transcripts.
   - Highlight tone and emphasis if relevant.
4. Cross-Modal Integration:
   - Reconcile any conflicts between modalities.
   - Produce a final answer that explicitly references how each modality influenced your conclusion.

### Output Skeleton

