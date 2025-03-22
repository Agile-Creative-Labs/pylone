/*init.js*/
// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  //const chatApp = new ChatApp();
   /*
   const chat = new WebSocketChat({
         url: 'ws://127.0.0.1:8001/chat',
         reconnectAttempts: 5,
         reconnectDelay: 3000,
         inactivityTimeout: 30000, // 30 seconds for testing
         autoReconnect: true,
         debug: false
     });
 */

  const chat = new FluwdChatApp({
    url: 'ws://127.0.0.1:8001/chat',
    reconnectAttempts: 5,
    reconnectDelay: 3000,
    inactivityTimeout: 30000,
    autoReconnect: true,
    debug: false
  });

});