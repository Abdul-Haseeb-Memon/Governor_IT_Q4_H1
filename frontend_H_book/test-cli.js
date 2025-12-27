#!/usr/bin/env node

/**
 * Command-line interface for testing frontend RAG components
 * Usage: node test-cli.js [command] [options]
 */

const { RAGService } = require('./components/RAGService');
const { validateQueryRequest } = require('./types/query');
const { validateAnswerResponse } = require('./types/response');

class RAGTestCLI {
  constructor() {
    this.ragService = new RAGService();
    this.commands = {
      'test-connection': this.testConnection.bind(this),
      'test-query': this.testQuery.bind(this),
      'test-retrieve': this.testRetrieve.bind(this),
      'test-answer': this.testAnswer.bind(this),
      'validate-query': this.validateQuery.bind(this),
      'validate-response': this.validateResponse.bind(this),
      'help': this.showHelp.bind(this)
    };
  }

  async run() {
    const args = process.argv.slice(2);
    const command = args[0] || 'help';
    const options = args.slice(1);

    if (this.commands[command]) {
      try {
        await this.commands[command](options);
      } catch (error) {
        console.error(`❌ Error executing command '${command}':`, error.message);
        process.exit(1);
      }
    } else {
      console.error(`❌ Unknown command: ${command}`);
      this.showHelp();
      process.exit(1);
    }
  }

  async testConnection() {
    console.log('🔍 Testing API connection...\n');

    try {
      const isConnected = await this.ragService.testConnection();

      if (isConnected) {
        console.log('✅ Connection test: PASSED');
        console.log(`📍 Connected to: ${this.ragService.getApiBaseUrl()}`);
      } else {
        console.log('❌ Connection test: FAILED');
        console.log(`📍 Attempted to connect to: ${this.ragService.getApiBaseUrl()}`);
      }
    } catch (error) {
      console.error('❌ Connection test failed with error:', error.message);
    }
  }

  async testQuery(options) {
    const query = options.join(' ') || 'What are the main components of the system?';

    console.log(`🔍 Testing query: "${query}"\n`);

    try {
      // Validate query
      const queryRequest = { query };
      if (!validateQueryRequest(queryRequest)) {
        console.log('❌ Query validation failed');
        return;
      }

      console.log('✅ Query validation: PASSED');

      // Test retrieve
      console.log('\n🔄 Testing context retrieval...');
      const context = await this.ragService.retrieveContext(query);
      console.log(`✅ Retrieved ${context.length} context chunks`);

      // Test answer generation
      console.log('\n🤖 Testing answer generation...');
      const response = await this.ragService.generateAnswer(query, context);

      console.log('✅ Answer generation: PASSED');
      console.log(`📝 Answer: ${response.answer.substring(0, 100)}${response.answer.length > 100 ? '...' : ''}`);
      console.log(`🔗 Sources: ${response.sources.length} references`);
      console.log(`📊 Confidence: ${response.confidence}`);
    } catch (error) {
      console.error('❌ Query test failed with error:', error.message);
    }
  }

  async testRetrieve(options) {
    const query = options.join(' ') || 'What are the main components?';

    console.log(`🔍 Testing retrieve for query: "${query}"\n`);

    try {
      const context = await this.ragService.retrieveContext(query);
      console.log(`✅ Retrieved ${context.length} context chunks`);

      if (context.length > 0) {
        console.log('📄 Sample context chunk:');
        console.log(`   Text: ${context[0].text ? context[0].text.substring(0, 100) + '...' : 'N/A'}`);
        console.log(`   Source: ${context[0].source_url || context[0].source || 'N/A'}`);
      }
    } catch (error) {
      console.error('❌ Retrieve test failed with error:', error.message);
    }
  }

  async testAnswer(options) {
    const query = options.join(' ') || 'What are the main components?';
    const context = [{ text: 'The system has multiple components that work together.', source_url: 'https://example.com/doc1' }];

    console.log(`🤖 Testing answer generation for query: "${query}"\n`);

    try {
      const response = await this.ragService.generateAnswer(query, context);

      console.log('✅ Answer generation: PASSED');
      console.log(`📝 Answer: ${response.answer}`);
      console.log(`🔗 Sources: ${response.sources.length} references`);
      console.log(`📊 Confidence: ${response.confidence}`);

      // Validate response
      if (validateAnswerResponse(response)) {
        console.log('✅ Response format validation: PASSED');
      } else {
        console.log('❌ Response format validation: FAILED');
      }
    } catch (error) {
      console.error('❌ Answer test failed with error:', error.message);
    }
  }

  validateQuery(options) {
    const query = options.join(' ') || 'What are the main components?';

    console.log(`🔍 Validating query: "${query}"\n`);

    const queryRequest = { query };
    const isValid = validateQueryRequest(queryRequest);

    if (isValid) {
      console.log('✅ Query validation: PASSED');
    } else {
      console.log('❌ Query validation: FAILED');
    }
  }

  validateResponse(options) {
    // Create a sample response for validation
    const response = {
      answer: "This is a sample answer from the system.",
      sources: ["https://example.com/doc1", "https://example.com/doc2"],
      confidence: 0.85
    };

    console.log('🔍 Validating response format...\n');
    console.log('Sample response:', JSON.stringify(response, null, 2));

    const isValid = validateAnswerResponse(response);

    if (isValid) {
      console.log('\n✅ Response validation: PASSED');
    } else {
      console.log('\n❌ Response validation: FAILED');
    }
  }

  showHelp() {
    console.log(`
🤖 RAG Chatbot Frontend Test CLI

Usage: node test-cli.js [command] [options]

Commands:
  test-connection          Test API connection to backend
  test-query [query]       Test full query flow (retrieve + answer)
  test-retrieve [query]    Test context retrieval only
  test-answer [query]      Test answer generation only
  validate-query [query]   Validate query format
  validate-response        Validate response format
  help                     Show this help message

Examples:
  node test-cli.js test-connection
  node test-cli.js test-query "What is RAG?"
  node test-cli.js test-retrieve "How does it work?"
  node test-cli.js validate-query "A valid query"
    `);
  }
}

// Run the CLI if this script is executed directly
if (require.main === module) {
  const cli = new RAGTestCLI();
  cli.run().catch(error => {
    console.error('CLI execution error:', error);
    process.exit(1);
  });
}

module.exports = RAGTestCLI;