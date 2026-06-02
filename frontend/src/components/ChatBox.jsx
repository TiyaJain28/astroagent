import { useState, useEffect, useRef } from "react";
import axios from "axios";
import Message from "./Message";

function ChatBox({ birthDetails }) {
  const [message, setMessage] = useState("");
const [messages, setMessages] = useState([
  {
    role: "assistant",
    content:
      "✨ Hello, I'm Aradhana. Ask me about your career, relationships, personality or today's cosmic energy.",
  },
]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: userMessage,
          date: birthDetails.date,
          time: birthDetails.time,
          place: birthDetails.place,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.data.response,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Something went wrong. Please try again.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>🔮 Chat with Aradhana</h2>

      <div className="chat-window">
        {messages.map((msg, index) => (
          <Message
            key={index}
            role={msg.role}
            content={msg.content}
          />
        ))}

        {loading && (
          <div className="typing">
            ✨ Aradhana is reading your chart...
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div className="input-row">
        <textarea
          rows="2"
          value={message}
          placeholder="Ask about career, love, personality..."
          onChange={(e) =>
            setMessage(e.target.value)
          }
        />

        <button onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatBox;