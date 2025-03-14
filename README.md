# Llama.Ipsum

A lightweight mock server that simulates the OpenAI API for development and testing purposes.

## Features

- [x] Implements key OpenAI API endpoints:
  - [x] `/v1/chat/completions`
  - [ ] `/v1/completions`
  - [ ] `/v1/models`
- [x] Supports API key authentication
- [x] Logs requests and responses
- [ ] Handles tool calls
- [ ] Supports streaming responses

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/taha-yassine/llama-ipsum.git
   cd llama-ipsum
   ```

2. Run the server:
   ```bash
   just run
   ```

## Template Customization

The mock server uses Jinja2 templates to generate responses. You can customize these templates to fit your specific testing needs.

### Using Custom Templates

1. **Create a directory for your custom templates**:
   ```bash
   mkdir -p my_templates
   ```

2. **Copy the templates you want to customize**:
   ```bash
   # Example: customize chat completion response
   cp app/templates/chat/completion.json.jinja my_templates/chat/
   ```

3. **Edit the templates** according to your needs.

4. **Start the server with your custom templates**:
   ```bash
   uv run -m app.main --template-dir /path/to/my_templates
   ```

## License

This project is licensed under the MIT License.
