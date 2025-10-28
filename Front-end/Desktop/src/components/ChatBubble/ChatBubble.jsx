import React from 'react';
import './styles.css';


// O nome do componente deve começar com letra maiúscula (convenção React)
function ChatBubble() {
    return (
        <div id="bubble"
            className="w-16 h-16 rounded-full bg-blue-600 cursor-pointer shadow-lg hover:scale-110 transition-transform flex items-center justify-center text-white text-2xl font-bold">
            A
        </div>
    );
}

export default ChatBubble;
