import "./App.css";
import {
  useSession,
  useSupabaseClient,
  useSessionContext,
} from "@supabase/auth-helpers-react";
import { DateTimePicker } from "react-datetime-picker";
import "react-datetime-picker/dist/DateTimePicker.css";
import "react-calendar/dist/Calendar.css";
import "react-clock/dist/Clock.css";
import { useState } from "react";

function App() {
  const [start, setStart] = useState(new Date());
  const [end, setEnd] = useState(new Date());
  const [eventName, setEventName] = useState("");
  const [description, setDescription] = useState("");

  const session = useSession(); // Tokens
  const supabase = useSupabaseClient(); //talk with the supabase
  const { isLoading } = useSessionContext();

  if (isLoading) {
    return <></>;
  }

  async function googleSingIn() {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        scopes:
          "https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events",
      },
    });

    if (error) {
      alert("Error logging in to google provider with Supabase");
      console.log(error);
    }
  }

  async function signOut() {
    await supabase.auth.signOut();
  }

  async function createTestEvent() {
    console.log("Creating a Test");
    const event = {
      summary: eventName,
      description: description,
      start: {
        dateTime: start.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      end: {
        dateTime: end.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      attendees: [{ email: "alejandro_gil91121@elpoli.edu.co" }],
    };
    console.log(event);
    const response = await fetch("http://127.0.0.1:8000/calendar/reserve_bot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(event),
    });

    const data = await response.json();
    console.log(data);
  }

  return (
    <div className="App">
      <div style={{ width: "400px", margin: "30px auto" }}>
        {session ? (
          <>
            <h2> Hey there {session.user.email}</h2>
            <p>Start of your test</p>
            <DateTimePicker onChange={setStart} value={start} />
            <p>End of your test</p>
            <DateTimePicker onChange={setEnd} value={end} />
            <p>Test Name</p>
            <input type="text" onChange={(e) => setEventName(e.target.value)} />
            <p>Test description (Optional)</p>
            <input
              type="text"
              onChange={(e) => setDescription(e.target.value)}
            />
            <hr />
            <button
              className="btn btn-primary"
              onClick={() => createTestEvent()}
            >
              {" "}
              Create Test Event
            </button>
            <p></p>
            <button className="btn btn-primary" onClick={() => signOut()}>
              Sign Out
            </button>
          </>
        ) : (
          <>
            <button onClick={() => googleSingIn()}>Sing In with Google</button>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
