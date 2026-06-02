function Message({ role, content }) {
  return (
    <div
      className={
        role === "user"
          ? "message user"
          : "message bot"
      }
    >
      {content}
    </div>
  );
}

export default Message;