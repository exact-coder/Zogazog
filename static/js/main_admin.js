/**
 * Variables
 */

const chatRoom = document.querySelector("#room_uuid").textContent.replaceAll('"','')
console.log(chatRoom);

let chatSocket = null;

/**
 * Elements
 */
const chatLogElement = document.querySelector("#chat_log");
const chatInputElement = document.querySelector("#chat_message_input");
const chatSubmitElement = document.querySelector("#chat_message_submit");



