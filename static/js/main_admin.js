/**
 * Variables
 */

const chatRoom = document.querySelector("#room_uuid").textContent.replaceAll('"','')
const userName =document.querySelector("#username").textContent.replaceAll('"','')
const agentId = document.querySelector("#user_id").textContent.replaceAll('"','')


let chatSocket = null;

/**
 * Elements
 */
const chatLogElement = document.querySelector("#chat_log");
const chatInputElement = document.querySelector("#chat_message_input");
const chatSubmitElement = document.querySelector("#chat_message_submit");

/**
 * Functions
 */


function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight;
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': userName,
        'agent': agentId,

    }))
    chatInputElement.value = ''
}

function onChatMessage(data){
    console.log('onChatMessage',data);

    if (data.type == 'chat_message') {
        let tmpInfo = document.querySelector('.tmp-info')

        if(tmpInfo) {
            tmpInfo.remove();
        }
        if (!data.agent) {
            chatLogElement.innerHTML += `
            <div class="flex w-full mt-2 space-x-3 max-w-md">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                <div>
                    <div style="background-color:rgb(209 213 219);" class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    <span class="text-xs text-gray-500 leading-none" >${data.created_at} ago</span>
                </div>
                
            </div>
            `
        }else{
            chatLogElement.innerHTML += `
            <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                <div>
                    <div style="background-color:rgb(147 197 253);" class="bg-blue-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    <span class="text-xs text-gray-500 leading-none" >${data.created_at} ago</span>
                </div>
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
            </div>
            `
        }
    }else if(data.type == 'writing_active'){
        if(!data.agent){
            let tmpInfo = document.querySelector('.tmp-info')

            if(tmpInfo) {
                tmpInfo.remove();
            }
            chatLogElement.innerHTML += `
                <div class="tmp-info flex w-full mt-2 space-x-3 max-w-md">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                    <div>
                        <div style="background-color:rgb(209 213 219);" class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">The client is typing...</p>
                        </div>
                    </div>
                    
                </div>
            `
        }
    }
    scrollToBottom()
}

/**
 * Web socket
 */

chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoom}/`)

chatSocket.onopen = function(e){
    console.log("On Open");
    scrollToBottom();
}

chatSocket.onmessage = function(e){
    console.log("On Message");
    onChatMessage(JSON.parse(e.data));
}

chatSocket.onclose = function(e){
    console.log("chat socket On Close unexpetedly");
}

/**
 * Event Listeners
 */

chatSubmitElement.onclick = function(e) {
    e.preventDefault()
    sendMessage()

    return false;
}

chatInputElement.onkeyup = function(e){
    if(e.keyCode == 13){
        sendMessage()
    }
}

chatInputElement.onfocus = function(e){
    chatSocket.send(JSON.stringify({
        'type': 'update',
        'message': 'writing_active',
        'name': userName,
        'agent': agentId,
    }))
}


