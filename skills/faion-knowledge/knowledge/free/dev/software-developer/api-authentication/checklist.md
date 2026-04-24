# Checklist

## Implementation

- [ ] User clicks "Login with Google"
- [ ] Redirect to: https://auth.example.com/authorize?
- [ ] User authenticates, grants permission
- [ ] Redirect to: https://app.com/callback?code=AUTH_CODE&state=random123
- [ ] Exchange code for tokens:

