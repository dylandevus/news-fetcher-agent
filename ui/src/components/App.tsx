import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PostsPage from "../pages/PostsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PostsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
