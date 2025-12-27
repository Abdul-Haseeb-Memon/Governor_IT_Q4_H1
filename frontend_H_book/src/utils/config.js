// Configuration file for API endpoints
// This file is built with environment variables during the build process

// Default configuration
const config = {
  // In Docusaurus deployed to Vercel, the environment variables should be available during build
  // If not, fall back to the custom fields set in docusaurus.config.ts
  API_BASE_URL: (function() {
    // Check for build-time environment variable first
    if (typeof process !== 'undefined' && process.env) {
      if (process.env.REACT_APP_API_BASE_URL) {
        return process.env.REACT_APP_API_BASE_URL;
      }
      if (process.env.API_BASE_URL) {
        return process.env.API_BASE_URL;
      }
    }

    // Then check for custom fields (runtime)
    if (typeof window !== 'undefined' && window.DOCUSAURUS_CUSTOM_FIELDS && window.DOCUSAURUS_CUSTOM_FIELDS.apiBaseUrl) {
      return window.DOCUSAURUS_CUSTOM_FIELDS.apiBaseUrl;
    }

    // Finally, fallback to default
    return 'https://governor-it-q4-h1.onrender.com'; // Default production URL
  })()
};

export default config;