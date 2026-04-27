/**
 * Pact consumer-side contract test template.
 * Replace 'Frontend', 'UserAPI', and interaction details for your service pair.
 * Run: jest pact-consumer.test.js
 * Output: pacts/Frontend-UserAPI.json (upload to PactFlow for provider verification)
 */
const { Pact, Matchers } = require('@pact-foundation/pact');
const path = require('path');

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserAPI',
  port: 8080,
  log: path.resolve(process.cwd(), 'logs', 'pact.log'),
  dir: path.resolve(process.cwd(), 'pacts'),
  logLevel: 'warn',
});

describe('UserAPI contract', () => {
  beforeAll(() => provider.setup());
  afterEach(() => provider.verify());
  afterAll(() => provider.finalize());

  describe('GET /users/:id', () => {
    it('returns user when user exists', async () => {
      await provider.addInteraction({
        state: 'user 123 exists',
        uponReceiving: 'a request for user 123',
        withRequest: {
          method: 'GET',
          path: '/users/123',
          headers: { Authorization: Matchers.like('Bearer token') },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: {
            id: Matchers.like('123'),
            name: Matchers.string('John'),
            email: Matchers.email(),
          },
        },
      });

      // Replace with your actual client call
      const response = await fetch('http://localhost:8080/users/123', {
        headers: { Authorization: 'Bearer token' },
      });
      const body = await response.json();
      expect(response.status).toBe(200);
      expect(body.id).toBeDefined();
    });
  });
});
