/**
 * Security audit for RAG Chatbot frontend code
 * Checks for common security issues
 */

const fs = require('fs');
const path = require('path');

class SecurityAuditor {
  constructor() {
    this.issues = [];
    this.securityScore = 100; // Start with perfect score, subtract for issues
  }

  async runAudit() {
    console.log('🔒 Running security audit...\n');

    // Audit all components
    await this.auditComponents();

    // Audit utilities
    await this.auditUtils();

    // Audit types
    await this.auditTypes();

    // Generate report
    this.generateReport();

    return this.issues.length === 0;
  }

  async auditComponents() {
    const componentsDir = path.join(__dirname, 'components');
    if (!fs.existsSync(componentsDir)) {
      console.log('❌ Components directory not found');
      return;
    }

    const files = fs.readdirSync(componentsDir);

    for (const file of files) {
      if (file.endsWith('.js') || file.endsWith('.jsx')) {
        const filePath = path.join(componentsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');

        console.log(`Auditing ${file}...`);

        // Check for XSS vulnerabilities
        this.checkForXSS(content, file);

        // Check for insecure API calls
        this.checkForInsecureAPI(content, file);

        // Check for hardcoded secrets
        this.checkForHardcodedSecrets(content, file);

        // Check for proper input validation
        this.checkForInputValidation(content, file);
      }
    }
  }

  async auditUtils() {
    const utilsDir = path.join(__dirname, 'utils');
    if (!fs.existsSync(utilsDir)) {
      console.log('❌ Utils directory not found');
      return;
    }

    const files = fs.readdirSync(utilsDir);

    for (const file of files) {
      if (file.endsWith('.js')) {
        const filePath = path.join(utilsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');

        console.log(`Auditing ${file}...`);

        // Check error handler for security
        this.checkForSecureErrorHandling(content, file);
      }
    }
  }

  async auditTypes() {
    const typesDir = path.join(__dirname, 'types');
    if (!fs.existsSync(typesDir)) {
      console.log('❌ Types directory not found');
      return;
    }

    const files = fs.readdirSync(typesDir);

    for (const file of files) {
      if (file.endsWith('.js')) {
        const filePath = path.join(typesDir, file);
        const content = fs.readFileSync(filePath, 'utf8');

        console.log(`Auditing ${file}...`);

        // Check for proper validation
        this.checkForSecureValidation(content, file);
      }
    }
  }

  checkForXSS(content, file) {
    // Check for potential XSS issues
    const dangerousPatterns = [
      /innerHTML/gi,
      /outerHTML/gi,
      /document\.write/gi,
      /eval\(/gi,
      /new Function/gi,
      /Function\(/gi,
      /setTimeout\(.*["'].*["']/gi,
      /setInterval\(.*["'].*["']/gi,
      /execScript/gi
    ];

    for (const pattern of dangerousPatterns) {
      if (pattern.test(content)) {
        const matches = content.match(pattern);
        this.issues.push({
          file,
          type: 'XSS_VULNERABILITY',
          description: `Potential XSS vulnerability found: ${matches[0]}`,
          severity: 'HIGH'
        });
        this.securityScore -= 20;
      }
    }
  }

  checkForInsecureAPI(content, file) {
    // Check for insecure HTTP calls
    if (/(http:|HTTP:)/.test(content) && !/(localhost|127\.0\.0\.1)/.test(content)) {
      this.issues.push({
        file,
        type: 'INSECURE_HTTP',
        description: 'Potential insecure HTTP call found (not localhost)',
        severity: 'HIGH'
      });
      this.securityScore -= 15;
    }
  }

  checkForHardcodedSecrets(content, file) {
    // Check for potential hardcoded secrets
    const secretPatterns = [
      /password\s*[:=]\s*["'][^"']*["']/gi,
      /secret\s*[:=]\s*["'][^"']*["']/gi,
      /token\s*[:=]\s*["'][^"']*["']/gi,
      /key\s*[:=]\s*["'][^"']*["']/gi,
      /api_key\s*[:=]\s*["'][^"']*["']/gi,
      /auth_token\s*[:=]\s*["'][^"']*["']/gi
    ];

    for (const pattern of secretPatterns) {
      if (pattern.test(content)) {
        this.issues.push({
          file,
          type: 'HARDCODED_SECRET',
          description: 'Potential hardcoded secret found',
          severity: 'CRITICAL'
        });
        this.securityScore -= 25;
      }
    }
  }

  checkForInputValidation(content, file) {
    // Check for proper input validation
    if (content.includes('input') && !content.includes('validate') && !content.includes('sanitize')) {
      // This is a very basic check - in a real audit, we'd want more sophisticated analysis
      if (content.includes('value') && content.includes('onChange')) {
        // Check if there's some form of validation
        if (!content.includes('validate') && !content.includes('.replace(') && !content.includes('sanitize')) {
          this.issues.push({
            file,
            type: 'INPUT_VALIDATION',
            description: 'Input validation may be missing',
            severity: 'MEDIUM'
          });
          this.securityScore -= 10;
        }
      }
    }
  }

  checkForSecureErrorHandling(content, file) {
    // Check that errors don't leak sensitive information
    if (content.toLowerCase().includes('error.message') && !content.includes('sanitize')) {
      this.issues.push({
        file,
        type: 'ERROR_LEAK',
        description: 'Error messages may leak sensitive information',
        severity: 'MEDIUM'
      });
      this.securityScore -= 5;
    }
  }

  checkForSecureValidation(content, file) {
    // Check for proper validation functions
    if (file.includes('query') || file.includes('response')) {
      if (!content.includes('validate') && !content.includes('sanitize')) {
        this.issues.push({
          file,
          type: 'MISSING_VALIDATION',
          description: 'Input validation may be missing in data type',
          severity: 'MEDIUM'
        });
        this.securityScore -= 8;
      }
    }
  }

  generateReport() {
    console.log('\n🛡️  Security Audit Report\n');

    if (this.issues.length === 0) {
      console.log('✅ No security issues found!');
      console.log(`🔒 Security Score: ${Math.max(0, this.securityScore)}/100`);
    } else {
      console.log(`❌ Found ${this.issues.length} security issue(s):\n`);

      const groupedIssues = this.issues.reduce((acc, issue) => {
        if (!acc[issue.severity]) acc[issue.severity] = [];
        acc[issue.severity].push(issue);
        return acc;
      }, {});

      for (const [severity, issues] of Object.entries(groupedIssues)) {
        console.log(`\n${severity} Severity Issues (${issues.length}):`);
        for (const issue of issues) {
          console.log(`  • ${issue.file}: ${issue.description} (${issue.type})`);
        }
      }

      console.log(`\n🔒 Security Score: ${Math.max(0, this.securityScore)}/100`);
    }

    console.log('\n💡 Recommendations:');
    console.log('• Always validate and sanitize user inputs');
    console.log('• Use environment variables for sensitive data');
    console.log('• Implement proper error handling without information leakage');
    console.log('• Avoid using eval() or Function() with user inputs');
    console.log('• Use HTTPS for all API communications');
  }
}

// Run audit if this script is executed directly
if (require.main === module) {
  const auditor = new SecurityAuditor();

  auditor.runAudit()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('Security audit error:', error);
      process.exit(1);
    });
}

module.exports = SecurityAuditor;