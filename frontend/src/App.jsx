import { useState } from "react";
import BirthForm from "./components/BirthForm";
import ChatBox from "./components/ChatBox";
import "./App.css";
function App() {
  const [birthDetails, setBirthDetails] = useState(null);

  return (
    <div className="app">

      <div className="stars"></div>
      <div className="shooting-star"></div>
      <div className="hero">
        <h1> AstroAgent</h1>
        <p>
          Your AI Astrology Companion
        </p>
      </div>

      {!birthDetails ? (
        <BirthForm
          onSubmit={(data) => {
            setBirthDetails(data);
          }}
        />
      ) : (
        <ChatBox birthDetails={birthDetails} />
      )}

    </div>
  );
}

export default App;

