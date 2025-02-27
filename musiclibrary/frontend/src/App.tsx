
import './App.css'
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from "./pages/Home"
import Library from "./pages/Library"
import Profile from "./pages/Profile"
import Search from "./pages/Search"
import Tracks from "./pages/Tracks"



function App() {


  return (
    <>
    <Router>
    <div>
    <Navbar/>
    <Routes>
      <Route path="/" element={<Home/>}></Route>
      <Route path="/library" element={<Library/>}></Route>
      <Route path="/search" element={<Search/>}></Route>
      <Route path="/profile" element={<Profile/>}></Route>
      <Route path="/tracks" element={<Tracks/>}></Route>
    </Routes>
    </div>
    </Router>
    </>
  )
}

export default App
