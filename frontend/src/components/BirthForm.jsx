import { useState } from "react";
import axios from "axios";

function BirthForm({ onSubmit }) {
  const [form, setForm] = useState({
    date: "",
    time: "",
    place: "",
  });

  const [saved, setSaved] =
    useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post(
        "http://127.0.0.1:8000/birth",
        form
      );

      setSaved(true);

      onSubmit(form);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form
      className="birth-form"
      onSubmit={handleSubmit}
    >
      <h2>🌙 Birth Details</h2>

      {saved && (
        <div className="success">
          ✨ Birth chart saved successfully
        </div>
      )}

      <input
        type="date"
        name="date"
        required
        onChange={handleChange}
      />

      <input
        type="time"
        name="time"
        required
        onChange={handleChange}
      />

      <input
        type="text"
        name="place"
        placeholder="Birth Place"
        required
        onChange={handleChange}
      />

      <button type="submit">
        Save Birth Details
      </button>
    </form>
  );
}

export default BirthForm;