const { sanitizeValue, sanitizeObject } = require('./packer');

describe('n8n-workflow-packer', () => {
  describe('sanitizeValue', () => {
    test('redacts sensitive webhook URLs while preserving protocol and path', () => {
      const url = 'https://my-n8n-instance.com/webhook/123-abc/active?token=xyz';
      const sanitized = sanitizeValue('webhookUrl', url);
      expect(sanitized).toBe('https://[REDACTED_HOST]/webhook/123-abc/active');
    });

    test('redacts simple URL errors fallback', () => {
      const invalidUrl = 'http://invalid-url-%%';
      const sanitized = sanitizeValue('webhookUrl', invalidUrl);
      expect(sanitized).toBe('https://[REDACTED_URL]');
    });

    test('redacts standard sensitive fields', () => {
      expect(sanitizeValue('api_key', 'super-secret-123')).toBe('[REDACTED_SECRET]');
      expect(sanitizeValue('password', 'my-password')).toBe('[REDACTED_SECRET]');
      expect(sanitizeValue('authToken', 'token-abc')).toBe('[REDACTED_SECRET]');
    });

    test('keeps non-sensitive values intact', () => {
      expect(sanitizeValue('name', 'My Node')).toBe('My Node');
      expect(sanitizeValue('version', 1)).toBe(1);
    });
  });

  describe('sanitizeObject', () => {
    test('recursively sanitizes nested objects and arrays', () => {
      const mockWorkflow = {
        name: 'My Test Workflow',
        nodes: [
          {
            parameters: {
              url: 'https://sensitive-service.com/api/v1',
              apiKey: 'sensitive-token'
            }
          }
        ]
      };

      const result = sanitizeObject(mockWorkflow);

      expect(result.name).toBe('My Test Workflow');
      expect(result.nodes[0].parameters.url).toBe('https://[REDACTED_HOST]/api/v1');
      expect(result.nodes[0].parameters.apiKey).toBe('[REDACTED_SECRET]');
    });

    test('redacts n8n credentials references structure', () => {
      const mockWorkflow = {
        nodes: [
          {
            credentials: {
              postgresDb: {
                id: '12',
                name: 'Prod Database Connection'
              }
            }
          }
        ]
      };

      const result = sanitizeObject(mockWorkflow);

      expect(result.nodes[0].credentials.postgresDb).toEqual({
        id: '[REDACTED_CREDENTIAL_ID]',
        name: '[REDACTED_CREDENTIAL_NAME]'
      });
    });
  });
});
