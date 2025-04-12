import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NewsPage from "./pages/NewsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
