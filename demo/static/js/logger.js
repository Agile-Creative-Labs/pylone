/**
 * Logger class to handle logging operations.
 *
 *  Author: Agile Creative Labs Inc.
 *  Date: 02 October 2024
 *  Version: 1.1.0
// Suggested Improvements:
// 1. Add more logging levels (e.g., warn, info, debug).
// 2. Implement a method to set the logging level dynamically.
// 3. Add timestamps to log messages for better traceability.
// 4. Consider using a logging library for more advanced features.

// Example usage:
/*
const logger = new Logger();
logger.log('This is a log message.');
logger.error('This is an error message.');
logger.disableLogging();
logger.log('This message will not be logged.');
logger.enableLogging();
logger.log('Logging is enabled again.');
*/
// Logger.js
/*
function Logger() {}

Logger.prototype.log = function(message) {
    console.log('[LOG]:', message);
};

Logger.prototype.error = function(message) {
    console.error('[ERROR]:', message);
};

Logger.prototype.warn = function(message) {
    console.warn('[WARN]:', message);
};
*/

/**
 * Logger class to handle logging operations.
 */
/**
 * @author Agile Creative Labs
 * @date 2023-11-25
 * @description A flexible logging utility class for JavaScript applications. 
 * Provides methods for logging messages at different levels (info, warn, error) with optional timestamp and prefix.
 */
class Logger 
{
    /**
     * Creates a new Logger instance.
     *
     * @param {string} prefix - Optional prefix to be added to log messages.
     * @param {boolean} logToFile - Flag to enable/disable file logging.
     */
    constructor(prefix = '', logToFile = false) {
        this.loggingEnabled = true;
        this.logLevel = 'info'; // Default log level
        this.prefix = prefix; // Optional prefix
        this.timestampFormat = 'iso'; // Default timestamp format
        this.logs = []; // Array to store logs in memory
        this.maxLogsInMemory = 1000; // Maximum number of logs in memory
        this.logToFile = false; // Flag to enable/disable file logging

        if (this.logToFile) {
            this.logFileName = 'logs.txt'; // Default log file name
            // Initialize the file (assumes a Cordova environment)
            this.initializeLogFile();
        }
    }

    /**
     * Gets the current timestamp in the desired format.
     *
     * @returns {string} The timestamp in the specified format.
     */
    getTimestamp() {
        return this.timestampFormat === 'local'
            ? new Date().toLocaleString()
            : new Date().toISOString();
    }

    /**
     * Logs a message with a timestamp.
     *
     * @param {string} level - The log level (e.g., 'info', 'warn', 'error').
     * @param {string} message - The message to log.
     */
    __logMessage(level, message) 
    {
        if (!this.loggingEnabled) return;

        const timestamp = this.getTimestamp();
        const logLevels = ['info', 'warn', 'error'];
        const messageLevelIndex = logLevels.indexOf(level);
        const logLevelIndex = logLevels.indexOf(this.logLevel);

        if (messageLevelIndex >= logLevelIndex) {
            const prefix = this.prefix ? `[${this.prefix}]` : '';
            const formattedMessage = `${prefix} [${timestamp}] [${level.toUpperCase()}]: ${message}`;

            // Store the log in memory
            this.logs.push(formattedMessage);
            // Ensure we don't exceed the max logs in memory
            if (this.logs.length > this.maxLogsInMemory) {
                this.logs.shift(); // Remove the oldest log
            }

            // Output to the console
            switch (level) {
                case 'info':
                    console.log(formattedMessage);
                    break;
                case 'warn':
                    console.warn(formattedMessage);
                    break;
                case 'error':
                    console.error(formattedMessage);
                    break;
                default:
                    console.log(`${prefix} [${timestamp}] [UNKNOWN]: ${message}`);
            }

            // Write to file if enabled
            if (this.logToFile) {
                this.writeLogToFile(formattedMessage);
            }
        }
    }
    //
    logMessage(level, message) 
    {
        if (!this.loggingEnabled) return;
    
        const timestamp = this.getTimestamp();
        const logLevels = ['info', 'warn', 'error'];
        const messageLevelIndex = logLevels.indexOf(level);
        const logLevelIndex = logLevels.indexOf(this.logLevel);
    
        if (messageLevelIndex >= logLevelIndex) {
            const prefix = this.prefix ? `[${this.prefix}]` : '';
            const formattedMessage = `${prefix} [${timestamp}] [${level.toUpperCase()}]: ${message}`;
    
            // Capture the stack trace conditionally
            let stackTrace = '';
            if (level === 'error' || level === 'warn') { // Only capture for error and warn levels
                const error = new Error();
                stackTrace = error.stack;
            }
    
            // Store the log in memory
            this.logs.push(`${formattedMessage}\nStack Trace: ${stackTrace}`);
            // Ensure we don't exceed the max logs in memory
            if (this.logs.length > this.maxLogsInMemory) {
                this.logs.shift(); // Remove the oldest log
            }
    
            // Output to the console
            switch (level) {
                case 'info':
                    console.log(formattedMessage);
                    break;
                case 'warn':
                    console.warn(formattedMessage);
                    console.warn(`Stack Trace: ${stackTrace}`);
                    break;
                case 'error':
                    console.error(formattedMessage);
                    console.error(`Stack Trace: ${stackTrace}`);
                    break;
                default:
                    console.log(`${prefix} [${timestamp}] [UNKNOWN]: ${message}`);
            }
    
            // Write to file if enabled
            if (this.logToFile) {
                this.writeLogToFile(`${formattedMessage}\nStack Trace: ${stackTrace}`);
            }
        }
    }
     //
    /**
     * Logs an info message.
     *
     * @param {string} message - The message to log.
     */
    log(message) {
        this.logMessage('info', message);
    }

    /**
     * Logs an error message.
     *
     * @param {string} message - The error message to log.
     */
    error(message) {
        this.logMessage('error', message);
    }

    /**
     * Logs a warning message.
     *
     * @param {string} message - The warning message to log.
     */
    warn(message) {
        this.logMessage('warn', message);
    }

    /**
     * Sets the log level.
     *
     * @param {string} level - The log level to set.
     */
    setLogLevel(level) {
        const validLevels = ['info', 'warn', 'error'];
        if (!validLevels.includes(level)) {
            console.error(`Invalid log level: ${level}`);
            return;
        }
        this.logLevel = level;
    }

    /**
     * Sets the timestamp format.
     *
     * @param {string} format - The timestamp format ('local' or 'iso').
     */
    setTimestampFormat(format) {
        this.timestampFormat = format === 'local' ? 'local' : 'iso';
    }

    /**
     * Disables logging.
     */
    disableLogging() {
        this.loggingEnabled = false;
    }

    /**
     * Enables logging.
     */
    enableLogging() {
        this.loggingEnabled = true;
    }

    /**
     * Retrieves all stored logs.
     *
     * @returns {Array} The array of stored logs.
     */
    getLogs() {
        return this.logs;
    }

    /**
     * Clears all stored logs.
     */
    clearLogs() {
        this.logs = [];
    }

    /**
     * Initializes the log file.
     */
    initializeLogFile() {
        document.addEventListener('deviceready', () => {
            window.resolveLocalFileSystemURL(cordova.file.dataDirectory, (dirEntry) => {
                dirEntry.getFile(this.logFileName, { create: true, exclusive: false }, (fileEntry) => {
                    this.log("Log file initialized.");
                }, (error) => {
                    console.error("Error initializing log file: " + error.code);
                });
            }, (error) => {
                console.error("Error resolving file system: " + error.code);
            });
        }, false);
    }

    /**
     * Writes a log message to the log file.
     *
     * @param {string} message - The log message to write.
     */
    writeLogToFile(message) 
    {
        document.addEventListener('deviceready', () => {
            window.resolveLocalFileSystemURL(cordova.file.dataDirectory, (dirEntry) => {
                dirEntry.getFile(this.logFileName, { create: false }, (fileEntry) => {
                    fileEntry.createWriter((fileWriter) => {
                        fileWriter.seek(fileWriter.length);
                        fileWriter.write(message + '\n');
                    }, (error) => {
                        console.error("Error writing to log file: " + error.code);
                    });
                }, (error) => {
                    console.error("Error getting log file: " + error.code);
                });
            }, (error) => {
                console.error("Error resolving file system: " + error.code);
            });
        }, false);
    }
    //
    errorPage(id, message) 
    {
        localStorage.setItem("error_id",id);
        localStorage.setItem("error_message",message);
        window.location.hash = "#error";
    }
}
