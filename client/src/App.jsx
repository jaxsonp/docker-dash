import "./index.css";
import "bootstrap/dist/css/bootstrap.css";
import { Routes, Route } from "react-router-dom";
import JobList from "./components/JobList";
import ServersView from "./components/ServersView";
import Layout from "./Layout";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<ServersView />} />
          <Route path="/:view/:viewId?" element={<JobList />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
