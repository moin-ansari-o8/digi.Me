# Security Policy

## Security Features

digi.Me implements several security measures to protect your data:

### 1. **Encrypted Storage**
- All chat messages are encrypted using Fernet (AES-128 CBC mode)
- Encryption key is derived from your ENCRYPTION_KEY in `.env`
- Database is stored locally, no cloud storage

### 2. **API Key Protection**
- API keys stored in `.env` file (excluded from git)
- Never hardcoded in source code
- Loaded securely via environment variables

### 3. **Approved Contacts**
- Whitelist-based contact filtering
- Only responds to pre-approved phone numbers
- Prevents unauthorized access to your AI twin

### 4. **Dashboard Authentication**
- Username/password protection for web interface
- Session-based authentication with secure cookies
- Configurable credentials in `.env`

### 5. **Secure Communication**
- Uses HTTPS for all AI API calls (OpenAI/Cohere)
- WhatsApp Web connection via official WhatsApp platform
- No third-party message interception

## Security Best Practices

### For Users

1. **Strong Encryption Key**
   ```bash
   # Generate a secure key
   openssl rand -base64 32
   # Or in Python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Protect `.env` File**
   - Never commit `.env` to version control
   - Set appropriate file permissions: `chmod 600 .env`
   - Don't share your `.env` file

3. **Change Default Credentials**
   ```env
   DASHBOARD_USERNAME=your_unique_username
   DASHBOARD_PASSWORD=strong_password_with_numbers_and_symbols_123!
   DASHBOARD_SECRET_KEY=generate_this_with_secrets_token_hex_32
   ```

4. **Verify Approved Contacts**
   - Only add trusted contacts to APPROVED_CONTACTS
   - Include country codes to prevent spoofing
   - Review approved contacts regularly

5. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

6. **Secure Your Host**
   - Don't expose dashboard port to the internet without proper firewall
   - Use localhost (127.0.0.1) for dashboard if not accessing remotely
   - Consider using a reverse proxy (nginx) with SSL for remote access

7. **Monitor API Usage**
   - Regularly check OpenAI/Cohere usage dashboards
   - Set spending limits on API provider accounts
   - Review generated responses for quality and safety

### For Developers

1. **Code Security**
   - Never log sensitive information (API keys, encryption keys)
   - Validate all user inputs
   - Use parameterized queries for database operations (already implemented)

2. **Dependency Management**
   - Run security audits: `pip-audit` or `safety check`
   - Keep dependencies up to date
   - Review dependency changelogs for security patches

3. **Testing**
   - Include security tests in test suite
   - Test input validation and sanitization
   - Verify encryption/decryption works correctly

## Vulnerability Reporting

If you discover a security vulnerability, please report it responsibly:

### DO:
- Email the maintainers directly with details
- Provide a clear description of the vulnerability
- Include steps to reproduce
- Give maintainers time to fix before public disclosure

### DON'T:
- Open a public GitHub issue for security vulnerabilities
- Exploit the vulnerability
- Share vulnerability details publicly before a fix is available

### What to Include:
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)
5. Your contact information for follow-up

## Known Limitations

### 1. **WhatsApp Session Security**
- Browser session stored in `/tmp/whatsapp-session`
- Consider encryption of session directory on shared systems
- Session can be invalidated from phone (WhatsApp → Linked Devices)

### 2. **Local Storage**
- Database stored locally without additional system-level encryption
- Relies on file system permissions and ENCRYPTION_KEY
- Consider full-disk encryption on your system

### 3. **Memory Safety**
- Encryption keys temporarily in memory during runtime
- Consider using secure memory management for production deployments

### 4. **Rate Limiting**
- No built-in rate limiting on dashboard
- Consider adding Fail2Ban or similar for production deployments

## Security Checklist

Before deploying digi.Me:

- [ ] Generated strong ENCRYPTION_KEY (32+ random characters)
- [ ] Changed default DASHBOARD_USERNAME and DASHBOARD_PASSWORD
- [ ] Generated secure DASHBOARD_SECRET_KEY
- [ ] Set proper file permissions on `.env` (chmod 600)
- [ ] Verified APPROVED_CONTACTS list is correct
- [ ] Updated all dependencies to latest secure versions
- [ ] Reviewed dashboard access settings (host/port)
- [ ] Set up firewall rules if exposing to network
- [ ] Configured API spending limits
- [ ] Tested backup and recovery procedures

## Compliance Notes

### Data Privacy
- All data is stored locally on your machine
- No data is sent to third parties except:
  - Messages to OpenAI/Cohere for response generation (per their privacy policies)
  - WhatsApp messages via official WhatsApp Web interface
- Review privacy policies of your AI provider

### GDPR Compliance
If handling EU citizen data:
- Encrypted storage helps with data protection requirements
- Local storage reduces data transfer concerns
- Consider data retention policies
- Implement right-to-be-forgotten (delete conversation features)

### Terms of Service
- Ensure compliance with WhatsApp Terms of Service
- Review OpenAI/Cohere Terms of Use
- This tool is for personal use; commercial use may require different licensing

## Security Updates

We take security seriously and will:
- Promptly address reported vulnerabilities
- Issue security patches in a timely manner
- Document security updates in CHANGELOG
- Notify users of critical security updates via GitHub releases

## Dependencies Security Status

Current dependency versions are checked against known vulnerabilities.
See `requirements.txt` for specific versions.

Last security audit: 2024-11-01

---

**Remember: Security is a shared responsibility. Follow best practices and keep your system secure!** 🔒
