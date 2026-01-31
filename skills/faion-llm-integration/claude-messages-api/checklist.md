# Claude Messages API - Checklist

## Basic Message Creation

- [ ] Create client with API key
- [ ] Build messages array with role/content
- [ ] Set max_tokens parameter
- [ ] Configure system prompt for behavior
- [ ] Handle response.content text extraction
- [ ] Parse response structure (id, type, role, model, usage)

## Parameters Configuration

- [ ] Set temperature (0.0 to 1.0)
- [ ] Configure top_p for nucleus sampling
- [ ] Set top_k for top-k sampling
- [ ] Define stop_sequences if needed
- [ ] Add metadata for request tracking
- [ ] Set appropriate max_tokens for response length

## Multi-turn Conversations

- [ ] Maintain message history array
- [ ] Append user and assistant messages
- [ ] Pass full conversation to each API call
- [ ] Extract assistant response and append
- [ ] Handle message limits for context size
- [ ] Implement conversation cleanup/archival

## Vision Implementation

- [ ] Encode images to base64 (PNG, JPEG, GIF, WebP)
- [ ] Support image URLs (https://)
- [ ] Build image content blocks with media type
- [ ] Handle PDF documents (up to 100 pages)
- [ ] Place images before text in content array
- [ ] Test high-resolution images for text extraction
- [ ] Support multiple images in single message

## Streaming Implementation

- [ ] Use client.messages.stream() context manager
- [ ] Implement text_stream iteration
- [ ] Handle event-based streaming (content_block_delta)
- [ ] Parse text_delta events from stream
- [ ] Collect final message with get_final_message()
- [ ] Implement async streaming with async context
- [ ] Handle tool_use streaming if applicable

## Response Processing

- [ ] Extract stop_reason (end_turn, max_tokens, stop_sequence, tool_use)
- [ ] Parse content blocks (text, tool_use, etc.)
- [ ] Handle tool_use blocks (name, input)
- [ ] Extract and track usage tokens
- [ ] Implement error handling for failed requests
- [ ] Log full response for debugging

## Testing & Validation

- [ ] Test basic message creation
- [ ] Test multi-turn conversations
- [ ] Test vision with various image formats
- [ ] Test streaming with large responses
- [ ] Verify token counting accuracy
- [ ] Test parameter effects on output quality
- [ ] Test with different models
