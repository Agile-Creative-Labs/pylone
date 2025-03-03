/**
 * FormValidator Class
 *
 * A generic class for validating form inputs to protect against security breaches.
 * This class provides methods to validate various types of input fields.
 *
 * @author Agile Creative Labs Inc.
 * @date 2025-03-02
 * @version 1.0.0
 *
 * Usage Example:
 *
 * // Initialize the validator
 * const validator = new FormValidator();
 *
 * // Validate a text input
 * const isValidText = validator.validateText('username', 'JohnDoe123');
 * console.log(isValidText); // Output: true or false
 *
 * // Validate an email input
 * const isValidEmail = validator.validateEmail('email', 'user@example.com');
 * console.log(isValidEmail); // Output: true or false
 *
 * // Validate a password input
 * const isValidPassword = validator.validatePassword('password', 'StrongPassword123!');
 * console.log(isValidPassword); // Output: true or false
 */
class FormValidator {
    /**
     * Validates a text input field.
     *
     * @param {string} fieldName - The name of the field being validated.
     * @param {string} value - The value of the field to validate.
     * @returns {boolean} - Returns true if the value is valid, false otherwise.
     */
    validateText(fieldName, value) {
      if (typeof value !== 'string' || value.trim() === '') {
        console.error(`${fieldName} is invalid. It must be a non-empty string.`);
        return false;
      }
      // Additional checks can be added here, such as length restrictions
      return true;
    }
  
    /**
     * Validates an email input field.
     *
     * @param {string} fieldName - The name of the field being validated.
     * @param {string} value - The value of the field to validate.
     * @returns {boolean} - Returns true if the value is a valid email, false otherwise.
     */
    validateEmail(fieldName, value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        console.error(`${fieldName} is invalid. It must be a valid email address.`);
        return false;
      }
      return true;
    }
  
    /**
     * Validates a password input field.
     *
     * @param {string} fieldName - The name of the field being validated.
     * @param {string} value - The value of the field to validate.
     * @returns {boolean} - Returns true if the value is a valid password, false otherwise.
     */
    validatePassword(fieldName, value) {
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
      if (!passwordRegex.test(value)) {
        console.error(`${fieldName} is invalid. It must be at least 8 characters long, include letters, numbers, and special characters.`);
        return false;
      }
      return true;
    }
  
    /**
     * Sanitizes an input value to prevent XSS attacks.
     *
     * @param {string} value - The value to sanitize.
     * @returns {string} - The sanitized value.
     */
    sanitizeInput(value) {
      const element = document.createElement('div');
      element.textContent = value;
      return element.innerHTML;
    }
  }
  
  // Example usage
  const validator = new FormValidator();
  
  const isValidText = validator.validateText('username', 'JohnDoe123');
  console.log(isValidText); // Output: true
  
  const isValidEmail = validator.validateEmail('email', 'user@example.com');
  console.log(isValidEmail); // Output: true
  
  const isValidPassword = validator.validatePassword('password', 'StrongPassword123!');
  console.log(isValidPassword); // Output: true
  
  const sanitizedInput = validator.sanitizeInput('<script>alert("XSS")</script>');
  console.log(sanitizedInput); // Output: &lt;script&gt;alert("XSS")&lt;/script&gt;
  