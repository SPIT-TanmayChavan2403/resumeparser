import './App.css';
import Home from './components/Home/Home'
import {Routes, Route, useLocation } from 'react-router-dom';
import Scorer from './components/Scorer/Scorer';


function App() {
  return (
    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/score" element={<Scorer />} />
    </Routes>
  );
}

export default App;
